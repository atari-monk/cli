import json
import logging
import os
from cli_app.cli_helpers import print_current_folder
from cli_app.config import COMMAND_NAME_MAX_LENGTH

logger = logging.getLogger(__name__)

def load_commands(folders, ignore_subfolders=["lib", "tests"]):
    """
    Load command files from the specified folder contexts.
    
    :param folders: List of folder paths to search for command files.
    :param ignore_subfolders: Subfolders to ignore during the search.
    :return: A dictionary where keys are folder paths and values are lists of command names.
    """
    if not isinstance(folders, list):
        raise TypeError("The 'folders' parameter must be a list of folder names.")

    folder_commands = {}

    for folder in folders:
        print(f"Processing folder: '{folder}'")
        logger.debug(f"Processing folder: '{folder}'")

        commands = []
        for _, dirs, files in os.walk(folder):
            # Filter out ignored subfolders
            dirs[:] = [d for d in dirs if d not in ignore_subfolders]

            for filename in files:
                if filename.endswith(".py") and filename != "__init__.py":
                    command_name = filename[:-3]
                    if len(command_name) > COMMAND_NAME_MAX_LENGTH:
                        raise ValueError(f"Command name '{command_name}' is too long. Maximum allowed length is {COMMAND_NAME_MAX_LENGTH} characters.")
                    commands.append(command_name)

        folder_commands[folder] = commands

    return folder_commands

import json

def generate_command_descriptions(folder_commands, descriptions_file='command_descriptions.json'):
    """
    Generate a list of command descriptions for each folder and its associated command files.

    Args:
        folder_commands (dict): A dictionary where each key is a folder name, and the value is a list of command file names (without extensions).
        descriptions_file (str): Path to the JSON file containing the descriptions.

    Returns:
        list: A list of dictionaries containing folder names and their commands with descriptions.
    """
    # Load the descriptions from the JSON file
    try:
        with open(descriptions_file, 'r') as f:
            descriptions_data = json.load(f)
    except Exception as e:
        print(f"Error reading descriptions file: {e}")
        return []

    folder_data = []

    # Loop through the folders and their command files
    for folder, command_files in folder_commands.items():
        commands = []
        
        # Find the corresponding folder in the descriptions data
        folder_descriptions = next(
            (folder_desc['commands'] for folder_desc in descriptions_data['folders'] if folder_desc['folder'] == folder), 
            []
        )

        # Loop through each command file and find its description
        for command_file in command_files:
            description = "Module not found"
            for cmd_desc in folder_descriptions:
                if cmd_desc["name"] == command_file:
                    description = cmd_desc["description"]
                    break

            commands.append({"name": command_file, "description": description})

        folder_data.append({"folder": folder, "commands": commands})

    return folder_data

def discover_folders(src_folder=".", ignore_folders=["cli_app", "shared", "lib", "tests"]):
    """
    Discover folders containing commands.
    """
    print_current_folder()
    folders = []
    for root, dirs, files in os.walk(src_folder):
        dirs[:] = [d for d in dirs if d not in ignore_folders]
        for folder in dirs:
            folder_path = os.path.join(root, folder)
            if "__init__.py" in os.listdir(folder_path):
                folders.append(folder)
    return folders
