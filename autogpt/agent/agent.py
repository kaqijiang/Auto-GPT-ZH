from colorama import Fore, Style

from autogpt.app import execute_command, get_command
from autogpt.chat import chat_with_ai, create_chat_message
from autogpt.config import Config
from autogpt.json_utils.json_fix_llm import fix_json_using_multiple_techniques
from autogpt.json_utils.utilities import validate_json
from autogpt.logs import logger, print_assistant_thoughts
from autogpt.speech import say_text
from autogpt.spinner import Spinner
from autogpt.utils import clean_input
from autogpt.localization import translate_command, translate_command_args


class Agent:
    """Agent class for interacting with Auto-GPT.

    Attributes:
        ai_name: 代理的名称
        memory: 要使用的内存对象
        full_message_history: 完整的消息历史记录
        next_action_count: 要执行的操作数
        system_prompt: 系统提示是初始提示，定义了AI需要了解的所有内容以成功完成任务。系统提示中的动态和可自定义信息包括ai_name、描述和目标
        triggering_prompt: AI在回答之前看到的最后一句话。对于Auto-GPT，这个提示是确定要使用哪个下一个命令，并使用上面指定的格式进行响应:
            The triggering prompt is not part of the system prompt because between the system prompt and the triggering
            prompt we have contextual information that can distract the AI and make it forget that its goal is to find the next task to achieve.
            SYSTEM PROMPT
            CONTEXTUAL INFORMATION (memory, previous conversations, anything relevant)
            TRIGGERING PROMPT

        The triggering prompt reminds the AI about its short term meta task (defining the next task)
    """

    def __init__(
        self,
        ai_name,
        memory,
        full_message_history,
        next_action_count,
        system_prompt,
        triggering_prompt,
    ):
        self.ai_name = ai_name
        self.memory = memory
        self.full_message_history = full_message_history
        self.next_action_count = next_action_count
        self.system_prompt = system_prompt
        self.triggering_prompt = triggering_prompt

    def start_interaction_loop(self):
        # Interaction Loop
        cfg = Config()
        loop_count = 0
        command_name = None
        arguments = None
        user_input = ""

        while True:
            # 检查是否达到了连续模式的限制
            loop_count += 1
            if (
                    cfg.continuous_mode
                    and 0 < cfg.continuous_limit < loop_count
            ):
                logger.typewriter_log(
                    "连续达到限制: ", Fore.YELLOW, f"{cfg.continuous_limit}"
                )
                break

            # 将消息发送给AI并获得响应
            with Spinner("正在思考... "):
                assistant_reply = chat_with_ai(
                    self.system_prompt,
                    self.triggering_prompt,
                    self.full_message_history,
                    self.memory,
                    cfg.fast_token_limit,
                )  # TODO: This hardcodes the model to use GPT3.5. Make this an argument

            assistant_reply_json = fix_json_using_multiple_techniques(assistant_reply)

            if not isinstance(assistant_reply_json, dict):
                logger.error(
                    "=" * 20 + "\n" +
                    f"修复JSON失败:\n"
                    f"原始回复: {assistant_reply}\n"
                    f"修复后的回复: {assistant_reply_json}"
                    + "\n" + "=" * 20
                )

            # 解析和验证AI的回复
            if assistant_reply_json != {}:
                validate_json(assistant_reply_json, "llm_response_format_1")
                # 从AI的回复中获取命令名称和参数
                try:
                    print_assistant_thoughts(self.ai_name, assistant_reply_json)
                    command_name, arguments = get_command(assistant_reply_json)
                    # command_name, arguments = assistant_reply_json_valid["command"]["name"], assistant_reply_json_valid["command"]["args"]
                    if cfg.speak_mode:
                        say_text(f"我要执行 {translate_command(command_name)}")
                except Exception as e:
                    logger.error("Error: \n", str(e))

            if not cfg.continuous_mode and self.next_action_count == 0:
                ### 根据配置，获取用户对执行命令的授权或直接执行命令 ###
                # Get key press: Prompt the user to press enter to continue or escape
                # to exit
                logger.typewriter_log(
                    "下一步操作: ",
                    Fore.CYAN,
                    f"指令 = {Fore.CYAN}{translate_command(command_name)}{Style.RESET_ALL}  "
                    f"参数 = {Fore.CYAN}{translate_command_args(arguments)}{Style.RESET_ALL}",
                )
                print(
                    f"输入'y'授权命令，'y -N'运行N个连续命令，'n'退出程序，或为{self.ai_name}输入反馈...",
                    flush=True)
                while True:
                    console_input = clean_input(
                        Fore.MAGENTA + "输入:" + Style.RESET_ALL
                    )
                    if console_input.lower().strip() == "y":
                        user_input = "GENERATE NEXT COMMAND JSON"
                        break
                    elif console_input.lower().strip() == "":
                        print("输入格式无效。")
                        continue
                    elif console_input.lower().startswith("y -"):
                        try:
                            self.next_action_count = abs(
                                int(console_input.split(" ")[1])
                            )
                            user_input = "GENERATE NEXT COMMAND JSON"
                        except ValueError:
                            print("输入格式无效。 请输入'y -n',其中 n 是连续任务的数量。 例如: y -1")
                            continue
                        break
                    elif console_input.lower() == "n":
                        user_input = "EXIT"
                        break
                    else:
                        user_input = console_input
                        command_name = "human_feedback"
                        break

                if user_input == "GENERATE NEXT COMMAND JSON":
                    logger.typewriter_log(
                        "-=-=-=-=-=-=-= 用户授权的命令 -=-=-=-=-=-=-=",
                        Fore.MAGENTA,
                        "",
                    )
                elif user_input == "EXIT":
                    print("退出中...", flush=True)
                    break
            else:
                # Print command
                logger.typewriter_log(
                    "下一步操作: ",
                    Fore.CYAN,
                    f"指令 = {Fore.CYAN}{translate_command(command_name)}{Style.RESET_ALL}"
                    f"  参数 = {Fore.CYAN}{translate_command_args(arguments)}{Style.RESET_ALL}",
                )

            # Execute command
            if command_name is not None and command_name.lower().startswith("error"):
                result = (
                    f"Command {command_name} 抛出以下错误: {arguments}"
                )
                result_localized = (
                    f"指令 {translate_command(command_name)} 抛出以下错误: {translate_command_args(arguments)}"
                )
            elif command_name == "human_feedback":
                result = f"人工反馈: {user_input}"
                result_localized = result
            else:
                result = (
                    f"Command {command_name} returned: "
                    f"{execute_command(command_name, arguments)}"
                )
                result_localized = (
                    f"指令 {translate_command(command_name)} 返回了: "
                    f"{execute_command(command_name, arguments)}"
                )
                if self.next_action_count > 0:
                    self.next_action_count -= 1

            memory_to_add = (
                f"机器人回复: {assistant_reply} "
                f"\n结果: {result} "
                f"\n人工反馈: {user_input} "
            )

            self.memory.add(memory_to_add)

            # 执行命令并将结果添加到内存和消息历史记录中
            # history
            if result is not None:
                self.full_message_history.append(create_chat_message("system", result))
                logger.typewriter_log("系统: ", Fore.YELLOW, result_localized)
            else:
                self.full_message_history.append(
                    create_chat_message("system", "无法执行命令")
                )
                logger.typewriter_log(
                    "SYSTEM: ", Fore.YELLOW, "无法执行命令"
                )
