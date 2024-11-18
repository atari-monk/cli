import json
import logging
from pathlib import Path
from cli_app.config import COMMAND_NAME_MAX_LENGTH
from shared.logger import setup_logger
import json

setup_logger(__name__)
logger = logging.getLogger(__name__)

def discover_folders_with_commands(
    src_folder_with_commands: str = ".",
    ignore_these_folders: list[str] = ["cli_app", "shared", "lib", "tests"]
) -> list[str]:
    src_path = Path(src_folder_with_commands)

    if not src_path.is_dir():
        logger.error(f"Specified source folder does not exist: {src_folder_with_commands}")
        return []

    ignore_set = {folder.lower() for folder in ignore_these_folders}

    folders = [
        folder.name
        for folder in src_path.rglob("*")
        if folder.is_dir()
        and folder.name.lower() not in ignore_set
        and (folder / "__init__.py").exists()
    ]

    logger.debug(f"Discovering folders...")
    logger.debug(f"Root: {src_folder_with_commands}")
    logger.debug(f"Ignored: {ignore_these_folders}")
    logger.debug(f"Discovered folders: {folders}")

    return sorted(folders)

def load_commands(
    folders: list[str], 
    ignore_subfolders: list[str] = ["lib", "tests"]
) -> dict[str, list[str]]:
    
    if not isinstance(folders, list):
        raise TypeError("The 'folders' parameter must be a list of folder names.")

    folder_commands = {}

    for folder in folders:
        folder_path = Path(folder)
        if not folder_path.is_dir():
            logger.warning(f"Folder does not exist or is not a directory: {folder}")
            continue

        logger.debug(f"Processing folder: {folder}")

        commands = []
        for subfolder in folder_path.rglob('*'):
            if subfolder.is_dir() and subfolder.name.lower() in ignore_subfolders:
                continue

            if subfolder.suffix == '.py' and subfolder.name != "__init__.py":
                command_name = subfolder.stem
                if len(command_name) > COMMAND_NAME_MAX_LENGTH:
                    raise ValueError(f"Command name '{command_name}' is too long. Maximum allowed length is {COMMAND_NAME_MAX_LENGTH} characters.")
                commands.append(command_name)

        folder_commands[str(folder_path)] = commands

    return folder_commands

def generate_command_descriptions(
    folder_commands: dict[str, list[str]], 
    descriptions_file: str = 'command_descriptions.json'
) -> list[dict]:
    try:
        with open(descriptions_file, 'r') as f:
            descriptions_data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        logger.error(f"Error reading descriptions file {descriptions_file}: {e}")
        return []

    folder_data = []

    folder_desc_map = {
        folder_desc['folder']: folder_desc['commands']
        for folder_desc in descriptions_data.get('folders', [])
    }

    for folder, command_files in folder_commands.items():
        folder_descriptions = folder_desc_map.get(folder, [])

        commands = [
            {
                "name": command_file,
                "description": next(
                    (cmd_desc["description"] for cmd_desc in folder_descriptions if cmd_desc["name"] == command_file), 
                    "Module not found"
                )
            }
            for command_file in command_files
        ]

        folder_data.append({"folder": folder, "commands": commands})

    return folder_data
