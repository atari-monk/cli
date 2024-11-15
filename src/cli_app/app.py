import sys

def print_help():
    print("Simple CLI App")
    print("Commands:")
    print("  help        - Show this help message")
    print("  exit        - Exit the program")
    print("  <command>   - Run a command with optional arguments")

def parse_input(user_input):
    # Split input into command and arguments
    parts = user_input.split()
    command = parts[0]
    args = parts[1:] if len(parts) > 1 else []
    return command, args

def main():
    print("Welcome to the Simple CLI App! Type 'help' for commands.")
    while True:
        # Prompt for user input
        user_input = input("> ").strip()

        # Handle the 'exit' command
        if user_input.lower() == "exit":
            print("Exiting the application.")
            break

        # Handle the 'help' command
        elif user_input.lower() == "help":
            print_help()

        else:
            # Parse and execute other commands
            command, args = parse_input(user_input)
            print(f"Command: {command}")
            if args:
                print(f"Arguments: {args}")
            else:
                print("No arguments provided.")

if __name__ == "__main__":
    main()
