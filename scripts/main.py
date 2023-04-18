from colorama import Style, init

# Initialize colorama
init(autoreset=True)

# Use the bold ANSI style
print(
    f"""{Style.BRIGHT}请 运行:
python -m autogpt
"""
)
