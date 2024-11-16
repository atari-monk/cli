import logging
import os
import importlib.util
from shared.logger import setup_logger

setup_logger(__name__)
logger = logging.getLogger(__name__)

COMMAND_NAME_MAX_LENGTH = 20

def load_commands(commands_folder="commands", ignore_folders=["lib", "tests"]):
    command_files = []
    
    for _, dirs, files in os.walk(commands_folder):
        dirs[:] = [d for d in dirs if d not in ignore_folders]
        
        for filename in files:
            if filename.endswith(".py") and filename != "__init__.py":
                command_name = filename[:-3]
                if len(command_name) > COMMAND_NAME_MAX_LENGTH:
                    raise ValueError(f"Command name '{command_name}' is too long. Maximum allowed length is 20 characters.")
                command_files.append(command_name)
    
    return command_files

import importlib.util
import importlib

def generate_command_descriptions(command_files):
    """
    Generate a list of command descriptions from a list of command files.

    Args:
        command_files (list): A list of command file names (without extensions).

    Returns:
        list: A list of dictionaries containing command names and their descriptions.
    """
    commands = []
    for command_file in command_files:
        module_name = f"commands.{command_file}"
        spec = importlib.util.find_spec(module_name)
        if spec is not None:
            command_module = importlib.import_module(module_name)
            description = getattr(command_module, 'description', 'No description available')
            commands.append({"name": command_file, "description": description})
        else:
            commands.append({"name": command_file, "description": "Module not found"})
    return commands

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

def print_help(commands):
    print("Simple CLI App")
    print("Commands:")
    lenght = COMMAND_NAME_MAX_LENGTH
    for command in commands:
        print(f"  {command['name']}{generate_spaces(lenght - len(command['name']))}- {command['description']}")
    print(f"  help{generate_spaces(lenght - len('help'))}- Show this help message")
    print(f"  exit{generate_spaces(lenght - len('exit'))}- Exit the program")

def parse_input(user_input):
    # Split input into command and arguments
    parts = user_input.split()
    command = parts[0]
    args = parts[1:] if len(parts) > 1 else []
    return command, args

def run_command(command_name):
    # Dynamically load the command module and run it
    module_name = f"commands.{command_name}"
    spec = importlib.util.find_spec(module_name)
    if spec is None:
        print(f"Command '{command_name}' not found.")
        return

    command_module = importlib.import_module(module_name)
    if hasattr(command_module, 'run'):
        command_module.run()
    else:
        print(f"Command '{command_name}' does not have a 'run' function.")
        
def main():
    print("Welcome to the Simple CLI App! Type 'help' for commands.")

     # Load all available commands
    commands = []
    command_files = load_commands()

    logger.debug(f"command_files: '{command_files}'")

    commands = generate_command_descriptions(command_files)

    while True:
        # Prompt for user input
        user_input = input("> ").strip()

        # Handle the 'exit' command
        if user_input.lower() == "exit":
            print("Exiting the application.")
            break

        # Handle the 'help' command
        elif user_input.lower() == "help":
            print_help(commands)

        else:
            # Parse and execute other commands
            command, args = parse_input(user_input)
            if command in [cmd['name'] for cmd in commands]:
                print(f"Command: {command}")
                if args:
                    print(f"Arguments: {args}")
                else:
                    print("No arguments provided.")
                run_command(command)
            else:
                print(f"Unknown command '{command}'. Type 'help' for a list of commands.")

if __name__ == "__main__":
    main()
