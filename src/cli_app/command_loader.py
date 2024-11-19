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

    folder_names = [
        folder.name
        for folder in src_path.rglob("*")
        if folder.is_dir()
        and folder.name.lower() not in ignore_set
        and (folder / "__init__.py").exists()
    ]

    logger.debug(f"Discovering folders...")
    logger.debug(f"Root: {src_folder_with_commands}")
    logger.debug(f"Ignored: {ignore_these_folders}")
    logger.debug(f"Discovered folders: {folder_names}")

    return sorted(folder_names)

def load_commands(
    folders: list[str], 
    descriptions_file: str = 'command_descriptions.json',
    ignore_subfolders: list[str] = ["lib", "tests"]
) -> dict[str, dict[str, dict[str, str]]]:
    
    if not isinstance(folders, list) or not all(isinstance(folder, str) for folder in folders):
        raise TypeError("The 'folders' parameter must be a list of folder names as strings.")

    folder_commands = {}

    try:
        with open(descriptions_file, 'r') as f:
            descriptions_data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        logger.error(f"Error reading descriptions file {descriptions_file}: {e}")
        descriptions_data = {}

    for folder in folders:
        folder_path = Path(folder)
        if not folder_path.is_dir():
            logger.warning(f"Folder does not exist or is not a directory: {folder}")
            continue

        logger.debug(f"Processing folder: {folder}")

        commands = {}
        for subfolder in folder_path.rglob('*.py'):
            if subfolder.is_dir() or subfolder.name.lower() in ignore_subfolders:
                continue

            if subfolder.name != "__init__.py":
                command_name = subfolder.stem
                if len(command_name) > COMMAND_NAME_MAX_LENGTH:
                    raise ValueError(f"Command name '{command_name}' is too long. Maximum allowed length is {COMMAND_NAME_MAX_LENGTH} characters.")

                description = descriptions_data.get(folder, {}).get(command_name, f"Description for {command_name} not found")
                commands[command_name] = description

        folder_commands[folder] = commands

    logger.debug(f"Discovered commands: {folder_commands}")
    return folder_commands
