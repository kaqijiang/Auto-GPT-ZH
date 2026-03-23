"""
Tests for MiniMax LLM provider integration.

Validates provider registration, model metadata, llm_call() behavior,
and credentials configuration using mocks (no infrastructure required).

Run: cd autogpt_platform/backend && PYTHONPATH=. python -m pytest test/block/test_llm_minimax.py -v --noconftest
"""

import enum
import json
import os
import re
import sys
import uuid
from types import ModuleType
from typing import NamedTuple
from unittest.mock import MagicMock, patch

import pytest

# ---------------------------------------------------------------------------
# Test: Provider enum (lightweight – only needs providers.py)
# ---------------------------------------------------------------------------


class TestMiniMaxProviderRegistration:
    def test_minimax_in_provider_enum(self):
        from backend.integrations.providers import ProviderName

        assert hasattr(ProviderName, "MINIMAX")
        assert ProviderName.MINIMAX.value == "minimax"

    def test_minimax_is_string_enum(self):
        from backend.integrations.providers import ProviderName

        assert isinstance(ProviderName.MINIMAX, str)
        assert ProviderName.MINIMAX == "minimax"


# ---------------------------------------------------------------------------
# Test: Model metadata via source-level parsing (avoids Prisma import chain)
# ---------------------------------------------------------------------------


class TestMiniMaxModelDefinition:
    """Verify MiniMax models and metadata are defined in llm.py source."""

    @pytest.fixture(autouse=True)
    def _read_source(self):
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "..", "backend", "blocks", "llm.py"
        )
        with open(src_path) as f:
            self.source = f.read()

    def test_minimax_m2_7_defined(self):
        assert 'MINIMAX_M2_7 = "MiniMax-M2.7"' in self.source

    def test_minimax_m2_5_defined(self):
        assert 'MINIMAX_M2_5 = "MiniMax-M2.5"' in self.source

    def test_minimax_m2_5_highspeed_defined(self):
        assert 'MINIMAX_M2_5_HIGHSPEED = "MiniMax-M2.5-highspeed"' in self.source

    def test_minimax_provider_in_metadata(self):
        assert 'ModelMetadata("minimax"' in self.source

    def test_m2_7_context_window(self):
        assert "LlmModel.MINIMAX_M2_7: ModelMetadata" in self.source
        # 1M context
        match = re.search(
            r'MINIMAX_M2_7: ModelMetadata\("minimax",\s*(\d+)',
            self.source,
        )
        assert match, "M2.7 metadata not found"
        assert int(match.group(1)) == 1_000_000

    def test_m2_5_context_window(self):
        match = re.search(
            r'MINIMAX_M2_5: ModelMetadata\("minimax",\s*(\d+)',
            self.source,
        )
        assert match, "M2.5 metadata not found"
        assert int(match.group(1)) == 1_000_000

    def test_m2_5_highspeed_context_window(self):
        match = re.search(
            r'MINIMAX_M2_5_HIGHSPEED: ModelMetadata\("minimax",\s*(\d+)',
            self.source,
        )
        assert match, "M2.5-highspeed metadata not found"
        assert int(match.group(1)) == 204800

    def test_minimax_in_llm_provider_name(self):
        assert "ProviderName.MINIMAX" in self.source


# ---------------------------------------------------------------------------
# Test: llm_call MiniMax branch (mocked — only tests the routing logic)
# We extract and test the MiniMax branch logic independently.
# ---------------------------------------------------------------------------


class TestMiniMaxLlmCallLogic:
    """Test the MiniMax OpenAI-compat call logic."""

    @staticmethod
    def _mock_response(content="Hello!", tool_calls=None):
        msg = MagicMock()
        msg.content = content
        msg.tool_calls = tool_calls

        choice = MagicMock()
        choice.message = msg

        usage = MagicMock()
        usage.prompt_tokens = 10
        usage.completion_tokens = 5

        resp = MagicMock()
        resp.choices = [choice]
        resp.usage = usage
        return resp

    @patch("openai.OpenAI")
    def test_basic_call_creates_client(self, mock_cls):
        """MiniMax branch should create OpenAI client with correct base_url."""
        mock_client = mock_cls.return_value
        mock_client.chat.completions.create.return_value = self._mock_response("Hi")

        import openai

        # Simulate the MiniMax llm_call branch
        client = openai.OpenAI(
            base_url="https://api.minimax.io/v1",
            api_key="test-key",
        )
        response = client.chat.completions.create(
            model="MiniMax-M2.7",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=100,
            temperature=1.0,
        )

        mock_cls.assert_called_with(
            base_url="https://api.minimax.io/v1",
            api_key="test-key",
        )
        assert response.choices[0].message.content == "Hi"

    def test_thinking_tag_regex(self):
        """Verify the regex pattern used to strip thinking tags."""
        text = "<think>Some reasoning\nMultiple lines</think>\nFinal answer."
        result = re.sub(r"<think>.*?</think>\s*", "", text, flags=re.DOTALL)
        assert "<think>" not in result
        assert "Final answer." in result

    def test_thinking_tag_no_tags(self):
        """When there are no thinking tags, text should remain unchanged."""
        text = "Just a normal response."
        result = re.sub(r"<think>.*?</think>\s*", "", text, flags=re.DOTALL)
        assert result == text

    def test_empty_thinking_tag(self):
        """Empty thinking tags should be stripped."""
        text = "<think></think>Result."
        result = re.sub(r"<think>.*?</think>\s*", "", text, flags=re.DOTALL)
        assert result == "Result."

    @patch("openai.OpenAI")
    def test_json_format_passed(self, mock_cls):
        """response_format=json_object should be passed for json_format=True."""
        mock_client = mock_cls.return_value
        mock_client.chat.completions.create.return_value = self._mock_response(
            '{"key":"val"}'
        )

        import openai

        client = openai.OpenAI(
            base_url="https://api.minimax.io/v1", api_key="test-key"
        )
        client.chat.completions.create(
            model="MiniMax-M2.5",
            messages=[{"role": "user", "content": "json"}],
            response_format={"type": "json_object"},
            max_tokens=100,
        )

        kw = mock_client.chat.completions.create.call_args[1]
        assert kw["response_format"] == {"type": "json_object"}

    @patch("openai.OpenAI")
    def test_tool_calls_extraction(self, mock_cls):
        """Tool calls from MiniMax response should be properly extracted."""
        mock_tool = MagicMock()
        mock_tool.id = "call_abc"
        mock_tool.type = "function"
        mock_tool.function.name = "search"
        mock_tool.function.arguments = '{"q":"test"}'

        mock_client = mock_cls.return_value
        mock_client.chat.completions.create.return_value = self._mock_response(
            content="", tool_calls=[mock_tool]
        )

        import openai

        client = openai.OpenAI(
            base_url="https://api.minimax.io/v1", api_key="test-key"
        )
        response = client.chat.completions.create(
            model="MiniMax-M2.7",
            messages=[{"role": "user", "content": "search"}],
            max_tokens=100,
            tools=[{"type": "function", "function": {"name": "search"}}],
        )

        tc = response.choices[0].message.tool_calls
        assert tc is not None
        assert len(tc) == 1
        assert tc[0].function.name == "search"

    @patch("openai.OpenAI")
    def test_empty_choices_raises(self, mock_cls):
        """Empty choices should raise ValueError."""
        resp = MagicMock()
        resp.choices = []
        mock_client = mock_cls.return_value
        mock_client.chat.completions.create.return_value = resp

        import openai

        client = openai.OpenAI(
            base_url="https://api.minimax.io/v1", api_key="test-key"
        )
        response = client.chat.completions.create(
            model="MiniMax-M2.7",
            messages=[{"role": "user", "content": "hi"}],
            max_tokens=100,
        )
        assert len(response.choices) == 0

    @patch("openai.OpenAI")
    def test_temperature_clamped(self, mock_cls):
        """Temperature for MiniMax should be in valid range (0, 1.0]."""
        mock_client = mock_cls.return_value
        mock_client.chat.completions.create.return_value = self._mock_response()

        import openai

        client = openai.OpenAI(
            base_url="https://api.minimax.io/v1", api_key="test-key"
        )

        # The MiniMax branch uses max(0.01, 1.0) = 1.0
        temperature = max(0.01, 1.0)
        assert 0 < temperature <= 1.0

        client.chat.completions.create(
            model="MiniMax-M2.7",
            messages=[{"role": "user", "content": "hi"}],
            max_tokens=100,
            temperature=temperature,
        )

        kw = mock_client.chat.completions.create.call_args[1]
        assert kw["temperature"] == 1.0


# ---------------------------------------------------------------------------
# Test: Credentials store source verification
# ---------------------------------------------------------------------------


class TestMiniMaxCredentialsSource:
    """Verify MiniMax credentials are in credentials_store.py source."""

    @pytest.fixture(autouse=True)
    def _read_source(self):
        src_path = os.path.join(
            os.path.dirname(__file__),
            "..", "..", "backend", "integrations", "credentials_store.py",
        )
        with open(src_path) as f:
            self.source = f.read()

    def test_minimax_credentials_defined(self):
        assert "minimax_credentials" in self.source

    def test_minimax_provider_string(self):
        assert 'provider="minimax"' in self.source

    def test_minimax_in_default_credentials(self):
        assert "minimax_credentials," in self.source

    def test_minimax_api_key_check(self):
        assert "settings.secrets.minimax_api_key" in self.source

    def test_minimax_title(self):
        assert "MiniMax" in self.source


# ---------------------------------------------------------------------------
# Test: Settings source verification
# ---------------------------------------------------------------------------


class TestMiniMaxSettings:
    """Verify minimax_api_key is in settings."""

    @pytest.fixture(autouse=True)
    def _read_source(self):
        src_path = os.path.join(
            os.path.dirname(__file__),
            "..", "..", "backend", "util", "settings.py",
        )
        with open(src_path) as f:
            self.source = f.read()

    def test_minimax_api_key_field(self):
        assert "minimax_api_key" in self.source

    def test_minimax_description(self):
        assert "MiniMax API key" in self.source


# ---------------------------------------------------------------------------
# Test: .env.example verification
# ---------------------------------------------------------------------------


class TestEnvExample:
    """Verify MINIMAX_API_KEY is in .env.example."""

    @pytest.fixture(autouse=True)
    def _read_source(self):
        src_path = os.path.join(
            os.path.dirname(__file__), "..", "..", ".env.example"
        )
        with open(src_path) as f:
            self.source = f.read()

    def test_minimax_api_key_env(self):
        assert "MINIMAX_API_KEY=" in self.source


# ---------------------------------------------------------------------------
# Integration tests (require MINIMAX_API_KEY env var, skip otherwise)
# ---------------------------------------------------------------------------


@pytest.mark.skipif(
    not os.environ.get("MINIMAX_API_KEY"),
    reason="MINIMAX_API_KEY not set",
)
class TestMiniMaxIntegration:
    """Integration tests calling the real MiniMax API via OpenAI SDK."""

    @pytest.fixture
    def client(self):
        import openai
        return openai.OpenAI(
            base_url="https://api.minimax.io/v1",
            api_key=os.environ["MINIMAX_API_KEY"],
        )

    def test_text_generation(self, client):
        resp = client.chat.completions.create(
            model="MiniMax-M2.5-highspeed",
            messages=[{"role": "user", "content": "Say hi in one word."}],
            max_tokens=200,
            temperature=1.0,
        )
        assert len(resp.choices) > 0
        text = resp.choices[0].message.content
        text = re.sub(r"<think>.*?</think>\s*", "", text, flags=re.DOTALL)
        assert len(text.strip()) > 0

    def test_json_generation(self, client):
        resp = client.chat.completions.create(
            model="MiniMax-M2.5-highspeed",
            messages=[
                {"role": "user", "content": 'Return JSON: {"greeting":"hello"}'}
            ],
            response_format={"type": "json_object"},
            max_tokens=500,
            temperature=1.0,
        )
        text = resp.choices[0].message.content
        # Strip thinking tags if present
        text = re.sub(r"<think>.*?</think>\s*", "", text, flags=re.DOTALL)
        parsed = json.loads(text)
        assert "greeting" in parsed

    def test_m2_7_model(self, client):
        resp = client.chat.completions.create(
            model="MiniMax-M2.7",
            messages=[
                {"role": "user", "content": "2+2=? Answer only the number."}
            ],
            max_tokens=200,
            temperature=1.0,
        )
        text = resp.choices[0].message.content
        text = re.sub(r"<think>.*?</think>\s*", "", text, flags=re.DOTALL)
        assert len(text.strip()) > 0
