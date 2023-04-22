"""Main script for the autogpt package."""
import click
from autogpt.localization import translate_memory_type


@click.group(invoke_without_command=True)
@click.option("-c", "--continuous", is_flag=True, help="启用连续模式")
@click.option(
    "--skip-reprompt",
    "-y",
    is_flag=True,
    help="跳过脚本开始时的重新提示信息。",
)
@click.option(
    "--ai-settings",
    "-C",
    help="指定要使用哪个 ai_settings.yaml 文件，也会自动跳过重新提示。",
)
@click.option(
    "-l",
    "--continuous-limit",
    type=int,
    help="定义在连续模式下运行的次数",
)
@click.option("--speak", is_flag=True, help="启用语音模式")
@click.option("--debug", is_flag=True, help="启用调试模式")
@click.option("--gpt3only", is_flag=True, help="启用 GPT3.5 Only Mode")
@click.option("--gpt4only", is_flag=True, help="启用 GPT4 Only Mode")
@click.option(
    "--use-memory",
    "-m",
    "memory_type",
    type=str,
    help="定义要使用哪个内存后端",
)
@click.option(
    "-b",
    "--browser-name",
    help="指定在使用Selenium爬取Web时要使用的Web浏览器.",
)
@click.option(
    "--allow-downloads",
    is_flag=True,
    help="危险：允许 Auto-GPT 本地下载文件。。这个选项可能允许 Auto-GPT 下载文件到本地计算机中，这可能会带来一些潜在的安全风险，因此需要格外小心使用.",
)
@click.option(
    "--skip-news",
    is_flag=True,
    help="指定是否在启动时不输出最新的消息.",
)
@click.pass_context
def main(
    ctx: click.Context,
    continuous: bool,
    continuous_limit: int,
    ai_settings: str,
    skip_reprompt: bool,
    speak: bool,
    debug: bool,
    gpt3only: bool,
    gpt4only: bool,
    memory_type: str,
    browser_name: str,
    allow_downloads: bool,
    skip_news: bool,
) -> None:
    """
    欢迎使用AutoGPT，这是一个实验性的开源应用程序，展示了GPT-4的能力，推动了人工智能的界限。

    启动一个Auto-GPT助手。
    """
    # Put imports inside function to avoid importing everything when starting the CLI
    import logging
    import sys

    from colorama import Fore

    from autogpt.agent.agent import Agent
    from autogpt.config import Config, check_openai_api_key
    from autogpt.configurator import create_config
    from autogpt.logs import logger
    from autogpt.memory import get_memory
    from autogpt.prompt import construct_prompt
    from autogpt.utils import get_current_git_branch, get_latest_bulletin

    if ctx.invoked_subcommand is None:
        cfg = Config()
        # TODO: fill in llm values here
        check_openai_api_key()
        create_config(
            continuous,
            continuous_limit,
            ai_settings,
            skip_reprompt,
            speak,
            debug,
            gpt3only,
            gpt4only,
            memory_type,
            browser_name,
            allow_downloads,
            skip_news,
        )
        logger.set_level(logging.DEBUG if cfg.debug_mode else logging.INFO)
        ai_name = ""
        if not cfg.skip_news:
            # motd = get_latest_bulletin()
            # if motd:
            #     logger.typewriter_log("NEWS: ", Fore.GREEN, motd)
            git_branch = get_current_git_branch()
            # if git_branch and git_branch != "stable":
            #     logger.typewriter_log(
            #         "警告：",
            #         Fore.RED,
            #         f"您正在运行 {git_branch} 分支 - 这不是受支持的分支。",
            #     )
            if sys.version_info < (3, 10):
                logger.typewriter_log(
                    "警告：",
                    Fore.RED,
                    "您正在运行旧版本的Python。某些人使用此版本会观察到Auto-GPT某些部分出现问题。请考虑升级到Python 3.10或更高版本。",
                )
        system_prompt = construct_prompt()
        # print(prompt)
        # Initialize variables
        full_message_history = []
        next_action_count = 0
        # Make a constant:
        triggering_prompt = (
            "确定要使用哪个下一个命令，并使用上面指定的格式进行响应："
        )
        # Initialize memory and make sure it is empty.
        # this is particularly important for indexing and referencing pinecone memory
        memory = get_memory(cfg, init=True)
        logger.typewriter_log(
            "使用记忆类型:", Fore.GREEN, f"{translate_memory_type(memory.__class__.__name__)}"
        )
        logger.typewriter_log("使用浏览器:", Fore.GREEN, cfg.selenium_web_browser)
        agent = Agent(
            ai_name=ai_name,
            memory=memory,
            full_message_history=full_message_history,
            next_action_count=next_action_count,
            system_prompt=system_prompt,
            triggering_prompt=triggering_prompt,
        )
        agent.start_interaction_loop()


if __name__ == "__main__":
    main()
