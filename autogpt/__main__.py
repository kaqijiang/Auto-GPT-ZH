"""Main script for the autogpt package."""
import logging
from colorama import Fore
from autogpt.agent.agent import Agent
from autogpt.args import parse_arguments

from autogpt.config import Config, check_openai_api_key
from autogpt.logs import logger
from autogpt.memory import get_memory

from autogpt.prompt import construct_prompt

# Load environment variables from .env file


def main() -> None:
    """Main function for the script"""
    cfg = Config()
    # TODO: fill in llm values here
    check_openai_api_key()
    parse_arguments()
    logger.set_level(logging.DEBUG if cfg.debug_mode else logging.INFO)
    ai_name = ""
    prompt = construct_prompt()
    # print(prompt)
    # Initialize variables
    full_message_history = []
    next_action_count = 0
    # Make a constant:
    user_input = "确定要使用的下一个命令，并使用上面指定的格式进行响应:"
    # Initialize memory and make sure it is empty.
    # this is particularly important for indexing and referencing pinecone memory
    memory = get_memory(cfg, init=True)
    logger.typewriter_log(
        f"使用存储的类型:", Fore.GREEN, f"{memory.__class__.__name__}"
    )
    logger.typewriter_log(f"使用浏览器:", Fore.GREEN, cfg.selenium_web_browser)
    agent = Agent(
        ai_name=ai_name,
        memory=memory,
        full_message_history=full_message_history,
        next_action_count=next_action_count,
        prompt=prompt,
        user_input=user_input,
    )
    agent.start_interaction_loop()


if __name__ == "__main__":
    main()
