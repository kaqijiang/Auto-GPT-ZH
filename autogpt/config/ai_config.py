# sourcery skip: do-not-use-staticmethod
"""
A module that contains the AIConfig class object that contains the configuration
"""
from __future__ import annotations

import os
from typing import Type

import yaml


class AIConfig:
    """
    一个包含 AI 配置信息的类对象

    Attributes:
        ai_name (str): AI名字
        ai_role (str): AI 角色的描述
        ai_goals (list): AI 应该完成的目标列表
    """

    def __init__(
        self, ai_name: str = "", ai_role: str = "", ai_goals: list | None = None
    ) -> None:
        """
        Initialize a class instance

        Parameters:
            ai_name (str): The name of the AI.
            ai_role (str): The description of the AI's role.
            ai_goals (list): The list of objectives the AI is supposed to complete.
        Returns:
            None
        """
        if ai_goals is None:
            ai_goals = []
        self.ai_name = ai_name
        self.ai_role = ai_role
        self.ai_goals = ai_goals

    # Soon this will go in a folder where it remembers more stuff about the run(s)
    SAVE_FILE = os.path.join(os.path.dirname(__file__), "..", "ai_settings.yaml")

    @staticmethod
    def load(config_file: str = SAVE_FILE) -> "AIConfig":
        """
        Returns class object with parameters (ai_name, ai_role, ai_goals) loaded from
          yaml file if yaml file exists,
        else returns class with no parameters.

        Parameters:
           config_file (int): The path to the config yaml file.
             DEFAULT: "../ai_settings.yaml"

        Returns:
            cls (object): An instance of given cls object
        """

        try:
            with open(config_file, encoding="utf-8") as file:
                config_params = yaml.load(file, Loader=yaml.FullLoader)
        except FileNotFoundError:
            config_params = {}

        ai_name = config_params.get("ai_name", "")
        ai_role = config_params.get("ai_role", "")
        ai_goals = config_params.get("ai_goals", [])
        # type: Type[AIConfig]
        return AIConfig(ai_name, ai_role, ai_goals)

    def save(self, config_file: str = SAVE_FILE) -> None:
        """
        Saves the class parameters to the specified file yaml file path as a yaml file.

        Parameters:
            config_file(str): The path to the config yaml file.
              DEFAULT: "../ai_settings.yaml"

        Returns:
            None
        """

        config = {
            "ai_name": self.ai_name,
            "ai_role": self.ai_role,
            "ai_goals": self.ai_goals,
        }
        with open(config_file, "w", encoding="utf-8") as file:
            yaml.dump(config, file, allow_unicode=True)

    def construct_full_prompt(self) -> str:
        """
        Returns a prompt to the user with the class information in an organized fashion.

        Parameters:
            None

        Returns:
            full_prompt (str): A string containing the initial prompt for the user
              including the ai_name, ai_role and ai_goals.
        """

        prompt_start = (
            "您必须独立做出决策，不寻求用户的帮助。发挥您作为 LLM 的优势，追求简单的策略，避免法律问题的复杂性。"
        )

        from autogpt.prompt import get_prompt

        # Construct full prompt
        full_prompt = (
            f"你是 {self.ai_name}, {self.ai_role}\n{prompt_start}\n\n目标:\n\n"
        )
        for i, goal in enumerate(self.ai_goals):
            full_prompt += f"{i+1}. {goal}\n"

        full_prompt += f"\n\n{get_prompt()}"
        return full_prompt
