import os
import importlib.util
import importlib

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
