import os
from cli_app.config import COMMAND_NAME_MAX_LENGTH

def generate_spaces(count):
    """
    Generates a string with the specified number of spaces.

    Args:
        count (int): The number of spaces to generate.

    Returns:
        str: A string containing 'count' spaces.
    """
    if count < 0:
        raise ValueError("Count must be a non-negative integer.")
    return ' ' * count

def print_help(folders, current_context):
    print("Simple CLI App")
    print("Commands:")
    length = COMMAND_NAME_MAX_LENGTH
    context_info = f" Selected folder: {current_context}" if current_context else " Selected folder: None"
    print(f"\n  {context_info}")

    # Build in commands
    print(f"\n  help{generate_spaces(length - len('help'))}- Show this help message")
    print(f"  exit{generate_spaces(length - len('exit'))}- Exit the program")
    print(f"  set_folder [folder_name]{generate_spaces(length - len('set_folder'))}- Set folder context")

    for folder_name, commands in folders.items():
        print(f"\n{folder_name} commands:")
        for command in commands:
            print(f"  {command['name']}{generate_spaces(length - len(command['name']))}- {command['description']}")

def print_current_folder():
    """
    Prints the current folder where the script is running.
    """
    current_folder = os.getcwd()
    print(f"Current working directory: {current_folder}")
