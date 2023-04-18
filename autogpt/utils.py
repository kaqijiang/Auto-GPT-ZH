import yaml
from colorama import Fore


def clean_input(prompt: str = ""):
    try:
        return input(prompt)
    except KeyboardInterrupt:
        print("您中断了 Auto-GPT")
        print("退出...")
        exit(0)


def validate_yaml_file(file: str):
    try:
        with open(file, encoding="utf-8") as fp:
            yaml.load(fp.read(), Loader=yaml.FullLoader)
    except FileNotFoundError:
        return (False, f"文件 {Fore.CYAN}`{file}`{Fore.RESET} 没有找到")
    except yaml.YAMLError as e:
        return (
            False,
            f"尝试读取 AI 设置文件时出现问题: {e}",
        )

    return (True, f"Successfully validated {Fore.CYAN}`{file}`{Fore.RESET}!")
