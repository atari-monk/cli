import importlib.util
import importlib
import logging
import shlex
from typing import Optional
from shared.logger import setup_logger

setup_logger(__name__)
logger = logging.getLogger(__name__)

def execute_user_input(user_input, folders, selected_folder):

    command, args = parse_input(user_input)

    matching_folders = find_command_in_folders(folders, command)

    if len(matching_folders) == 1:
        selected_folder = matching_folders[0]
        print(f"Automatically selected folder: {selected_folder}")
        run_command(selected_folder, command, args)
    elif len(matching_folders) > 1:
        selected_folder = display_menu(matching_folders)
        run_command(selected_folder, command, args)
    else:
        print(f"Unknown command '{command}'. Type 'help' for a list of commands.")

def parse_input(user_input: str) -> tuple[str, list[str]]:
    if not user_input.strip():
        return '', []

    parts = shlex.split(user_input)
    command = parts[0]
    args = parts[1:]
    return command, args

def find_command_in_folders(folders: dict[str, dict[str, dict[str, str]]], command_name: str) -> list[str]:
    return [folder_name for folder_name, commands in folders.items() if command_name in commands]

def run_command(selected_folder: str, command: str, args: Optional[list[str]] = None) -> None:
    args = args or []
    
    module_name = f"{selected_folder}.{command}"
    logger.debug(f"Attempting to find module: {module_name}")
    
    spec = importlib.util.find_spec(module_name)
    if spec is None:
        logger.error(f"Command '{command}' not found in folder '{selected_folder}'.")
        return

    try:
        command_module = importlib.import_module(module_name)
    except Exception as e:
        logger.exception(f"Failed to import module '{module_name}'. Error: {e}")
        return

    if hasattr(command_module, 'run'):
        try:
            logger.info(f"Running command '{command}' with arguments: {args}")
            command_module.run(args)
        except Exception as e:
            logger.exception(f"An error occurred while executing the 'run' function in '{module_name}'. Error: {e}")
    else:
        logger.warning(f"Command '{command}' does not have a 'run' function.")

def display_menu(options: list[str]) -> str:
    logger.info("Multiple folders contain this command:")
    for index, option in enumerate(options, start=1):
        logger.info(f"{index}. {option}")
    
    return get_valid_choice(options)

def get_valid_choice(options: list[str]) -> str:
    while True:
        try:
            choice = input("Select a folder by number: ").strip()
            if choice.isdigit():
                choice = int(choice) - 1
                if 0 <= choice < len(options):
                    return options[choice]
                else:
                    logger.info(f"Invalid choice. Please choose a number between 1 and {len(options)}.")
            else:
                raise ValueError
        except ValueError:
            logger.error("Invalid input. Please enter a valid number.")
