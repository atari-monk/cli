import os
from typing import Optional
from cli_app.config import COMMAND_NAME_MAX_LENGTH

def generate_string(count: int, string: str = ' ', max_length: int = 1000) -> str:
    result = string * count
    if len(result) > max_length:
        raise ValueError(f"The resulting string exceeds the maximum allowed length of {max_length}.")
    return result

def generate_padding(length: int, string: str) -> str:
    padding_length = length - len(string)
    if padding_length < 0:
        return ''
    return generate_string(padding_length)

def get_help(folders: dict[str, dict[str, dict[str, str]]], selected_folder: Optional[str]) -> None:
    help = []
    
    help.append("Simple CLI App")
    help.append("Commands:")
    
    selected_folder_info = f" Selected folder: {selected_folder}" if selected_folder else " Selected folder: None"
    help.append(f"\n  {selected_folder_info}")
    
    length = COMMAND_NAME_MAX_LENGTH
    help.append(f"\n  help{generate_padding(length, 'help')}- Show this help message")
    help.append(f"  exit{generate_padding(length, 'exit')}- Exit the program")
    help.append(f"  set_folder [folder_name]{generate_padding(length, 'set_folder')}- Set folder context")
    
    for folder_name, commands in folders.items():
        help.append(f"\n{folder_name} commands:")
        for command_name, command_info in commands.items():
            help.append(f"  {command_name}{generate_padding(length, command_name)}- {command_info['description']}")
    
    return "\n".join(help)

def get_current_working_directory():
    current_folder = os.getcwd()
    return f"Current working directory: {current_folder}"
