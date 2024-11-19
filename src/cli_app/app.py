import logging
from cli_app.cli_helpers import print_current_folder, print_help
from cli_app.command_loader import discover_folders_with_commands, load_commands
from cli_app.command_runner import execute_user_input
from shared.logger import setup_logger

setup_logger(__name__)
logger = logging.getLogger(__name__)

def main():
    logger.info("Welcome to the Simple CLI App! Type 'help' for commands.")

    print_current_folder()

    selected_folder = None

    folders = discover_folders_with_commands()

    commands = load_commands(folders)
    
    while True:
        # Prompt for user input
        user_input = input("> ").strip()

        # Handle the 'exit' command
        if user_input.lower() == "exit":
            print("Exiting the application.")
            break

        # Handle the 'help' command
        elif user_input.lower() == "help":
            print_help(commands, selected_folder)

        elif user_input.lower().startswith("set_folder"):
            folder_name = user_input.split(maxsplit=1)[-1]
            if folder_name in folders:
                #global current_context
                selected_folder = folder_name
                print(f"Folder context set to: {folder_name}")
                #folder_commands = load_commands(selected_folder)
                #logger.debug(f"command_files: '{folder_commands}'")
                #commands = generate_command_descriptions(folder_commands, selected_folder)
                #logger.debug(f"commands: '{commands}'")
            else:
                print(f"Folder '{folder_name}' not found. Available: {folders}")
                
        else:
            # Parse and execute other commands
            execute_user_input(user_input, commands, selected_folder)

if __name__ == "__main__":
    main()
