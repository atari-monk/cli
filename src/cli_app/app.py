import logging
from cli_app.cli_helpers import print_help
from cli_app.command_loader import generate_command_descriptions, load_commands
from cli_app.command_runner import run_command
from shared.logger import setup_logger

setup_logger(__name__)
logger = logging.getLogger(__name__)

def parse_input(user_input):
    # Split input into command and arguments
    parts = user_input.split()
    command = parts[0]
    args = parts[1:] if len(parts) > 1 else []
    return command, args

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
