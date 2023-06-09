from colorama import Fore

from autogpt.config.ai_config import AIConfig
from autogpt.config.config import Config
from autogpt.llm import ApiManager
from autogpt.logs import logger
from autogpt.prompts.generator import PromptGenerator
from autogpt.setup import prompt_user
from autogpt.utils import clean_input

CFG = Config()

DEFAULT_TRIGGERING_PROMPT = (
    "Determine which next command to use, and respond using the format specified above:"
)


def build_default_prompt_generator() -> PromptGenerator:
    """
    This function generates a prompt string that includes various constraints,
        commands, resources, and performance evaluations.

    Returns:
        str: The generated prompt string.
    """

    # # Initialize the PromptGenerator object
    # prompt_generator = PromptGenerator()

    # # Add constraints to the PromptGenerator object
    # prompt_generator.add_constraint(
    #     "~4000 word limit for short term memory. Your short term memory is short, so"
    #     " immediately save important information to files."
    # )
    # prompt_generator.add_constraint(
    #     "If you are unsure how you previously did something or want to recall past"
    #     " events, thinking about similar events will help you remember."
    # )
    # prompt_generator.add_constraint("No user assistance")
    # # prompt_generator.add_constraint("Please localize natural language strings in your reply to Chinese")
    
    # prompt_generator.add_constraint("Reply must be in Chinese")
    # prompt_generator.add_constraint("If the content of the reply is not in Chinese, you need to translate it into Chinese")
    # prompt_generator.add_constraint(
    #     'Exclusively use the commands listed in double quotes e.g. "command name"'
    # )

    # # Define the command list
    # commands = [
    #     ("Task Complete (Shutdown)", "task_complete", {"reason": "<reason>"}),
    # ]

    # # Add commands to the PromptGenerator object
    # for command_label, command_name, args in commands:
    #     prompt_generator.add_command(command_label, command_name, args)

    # # Add resources to the PromptGenerator object
    # prompt_generator.add_resource(
    #     "Internet access for searches and information gathering."
    # )
    # prompt_generator.add_resource("Long Term memory management.")
    # prompt_generator.add_resource(
    #     "GPT-3.5 powered Agents for delegation of simple tasks."
    # )
    # prompt_generator.add_resource("File output.")

    # # Add performance evaluations to the PromptGenerator object
    # prompt_generator.add_performance_evaluation(
    #     "Continuously review and analyze your actions to ensure you are performing to"
    #     " the best of your abilities."
    # )
    # prompt_generator.add_performance_evaluation(
    #     "Constructively self-criticize your big-picture behavior constantly."
    # )
    # prompt_generator.add_performance_evaluation(
    #     "Reflect on past decisions and strategies to refine your approach."
    # )
    # prompt_generator.add_performance_evaluation(
    #     "Every command has a cost, so be smart and efficient. Aim to complete tasks in"
    #     " the least number of steps."
    # )
    # prompt_generator.add_performance_evaluation("Write all code to a file.")

    prompt_generator = PromptGenerator()

    # 向PromptGenerator对象添加约束条件
    prompt_generator.add_constraint(
        "~4000字的短期记忆限制。由于您的短期记忆较短，因此请立即将重要信息保存到文件中。"
    )
    prompt_generator.add_constraint(
        "如果您不确定以前如何做某事或想回忆过去的事件，思考类似的事件将有助于您记忆。"
    )
    prompt_generator.add_constraint("无用户辅助")
    # prompt_generator.add_constraint("请在回复中将自然语言字符串本地化为中文")

    prompt_generator.add_constraint("回复必须为中文")
    prompt_generator.add_constraint("如果回复内容不是中文，则需要将其翻译为中文")
    prompt_generator.add_constraint(
        '仅使用双引号中列出的命令，例如"command name"'
    )

    # 定义命令列表
    commands = [    ("任务完成（关闭）", "task_complete", {"reason": "<reason>"}),]

    # 向PromptGenerator对象添加命令
    for command_label, command_name, args in commands:
        prompt_generator.add_command(command_label, command_name, args)

    # 向PromptGenerator对象添加资源
    prompt_generator.add_resource(
        "互联网访问以进行搜索和信息收集。"
    )
    prompt_generator.add_resource("长期记忆管理。")
    prompt_generator.add_resource(
        "由GPT-3.5提供支持的代理人用于简单任务的委派。"
    )
    prompt_generator.add_resource("文件输出。")

    # 向PromptGenerator对象添加绩效评估
    prompt_generator.add_performance_evaluation(
        "持续审查和分析您的行为，以确保您尽最大努力发挥能力。"
    )
    prompt_generator.add_performance_evaluation(
        "持续对自己的总体行为进行建设性的自我批评。"
    )
    prompt_generator.add_performance_evaluation(
        "反思过去的决策和策略，以完善您的方法。"
    )
    prompt_generator.add_performance_evaluation(
        "每个命令都有成本，因此要聪明和高效。目标是以最少的步骤完成任务。"
    )
    prompt_generator.add_performance_evaluation("将所有代码写入文件。")

    return prompt_generator


def construct_main_ai_config() -> AIConfig:
    """Construct the prompt for the AI to respond to

    Returns:
        str: The prompt string
    """
    config = AIConfig.load(CFG.ai_settings_file)
    if CFG.skip_reprompt and config.ai_name:
        logger.typewriter_log("名称 :", Fore.GREEN, config.ai_name)
        logger.typewriter_log("职责 :", Fore.GREEN, config.ai_role)
        logger.typewriter_log("目标:", Fore.GREEN, f"{config.ai_goals}")
        logger.typewriter_log(
            "API预算:",
            Fore.GREEN,
            "无限" if config.api_budget <= 0 else f"${config.api_budget}",
        )
    elif config.ai_name:
        logger.typewriter_log(
            "欢迎回来! ",
            Fore.GREEN,
            f"你想让 {config.ai_name} 继续执行原来的任务吗?",
            speak_text=True,
        )
        should_continue = clean_input(
            f"""继续上次的这些设置?
名称:  {config.ai_name}
角色:  {config.ai_role}
目标: {config.ai_goals}
API预算: {"无限" if config.api_budget <= 0 else f"${config.api_budget}"}
继续 ({CFG.authorise_key}/{CFG.exit_key}): """
        )
        if should_continue.lower() == CFG.exit_key:
            config = AIConfig()

    if not config.ai_name:
        config = prompt_user()
        config.save(CFG.ai_settings_file)

    # set the total api budget
    api_manager = ApiManager()
    api_manager.set_total_budget(config.api_budget)

    # Agent Created, print message
    logger.typewriter_log(
        config.ai_name,
        Fore.LIGHTBLUE_EX,
        "已创建并包含以下详细信息：",
        speak_text=True,
    )

    # Print the ai config details
    # Name
    logger.typewriter_log("名称:", Fore.GREEN, config.ai_name, speak_text=False)
    # Role
    logger.typewriter_log("角色:", Fore.GREEN, config.ai_role, speak_text=False)
    # Goals
    logger.typewriter_log("目标:", Fore.GREEN, "", speak_text=False)
    for goal in config.ai_goals:
        logger.typewriter_log("-", Fore.GREEN, goal, speak_text=False)

    return config
