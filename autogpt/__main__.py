"""Auto-GPT: A GPT powered AI Assistant"""
import autogpt.cli
import autogpt.localization

if __name__ == "__main__":
    print("Auto-GPT 正在启动...")
    autogpt.localization.hook_open()
    autogpt.cli.main()
