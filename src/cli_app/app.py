import logging
from typing import Optional
from shared.logger import setup_logger
from cli_app.cli_helpers import get_current_working_directory, get_help
from cli_app.command_loader import discover_folders_with_commands, load_commands
from cli_app.command_runner import execute_user_input

setup_logger(__name__)
logger = logging.getLogger(__name__)

def main() -> None:
    logger.info("Welcome to the Simple CLI App! Type 'help' for commands.")
    logger.info(get_current_working_directory())

    selected_folder: Optional[str] = None

    folders = discover_folders_with_commands()
    commands = load_commands(folders)

    while True:
        user_input = input("> ").strip()

        if user_input.lower() == "exit":
            logger.info("Exiting the application.")
            break

        elif user_input.lower() == "help":
            logger.info(get_help(commands, selected_folder))

        elif user_input.lower().startswith("set_folder"):
            folder_name = user_input.split(maxsplit=1)[-1]
            if folder_name in folders:
                selected_folder = folder_name
                logger.info(f"Folder context set to: {folder_name}")
            else:
                logger.info(f"Folder '{folder_name}' not found. Available: {folders}")                
        else:
            execute_user_input(user_input, commands, selected_folder)

if __name__ == "__main__":
    main()
