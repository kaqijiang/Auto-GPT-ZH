"""Auto-GPT: A GPT powered AI Assistant"""
import autogpt.cli
import autogpt.localization

if __name__ == "__main__":
    
    autogpt.localization.hook_open()
    autogpt.cli.main()
