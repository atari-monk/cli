# Cli app

Notes for py cli app, to aid project.

## Project Assumptions

### Project structure

```plaintext
cli/                            # Root folder of repository
├── doc/                        # Notes
│   └── cli_app.md              # Project notes
└── src/                        # Source code folder
│   └── cli_app/                # CLI application module
│   │   ├── __init__.py         # Module initializer
│   │   ├── app.py              # Main CLI logic
│   └── log_project/            # Log project module
│   │   ├── __init__.py         # Module initializer
│   │   ├── lib                 # Code
|   |   |   ├── __init__.py     # Module initializer
|   │   ├── tests               # Tests
|   │   ├──                     # Commands src
|   └── shared/                 # Shared code
|       ├── __init__.py         # Module initializer
|       ├──                     # Shared src
|       ├── tests               # Tests
├── .gitignore                  # Git ignore rules
├── README.md                   # Project documentation
├── requirements.txt            # Dependencies list
```

### File name convention

1. For py, md files:
   -lowercase
   -underscores separators

```plaintext
file_system.py
```

### .gitignore

Elements added to .gitignore in project started from scratch. In order of appearance.

```plaintext
__pycache__
.pytest_cache
cli_app.log
```

### init file

```plaintext
__init__.py
```

Marks directory as package, that means file are modules for import.
Should generally be committed to version control.

### Tests

In tests folders. Using pytest.
Naming convention:

```plaintexy
 test_*.py.
```

To test shared files i used this assumptions.
I cd to shared folder.
Run command

```bash
pytest tests
```

This will work when relative import, from folder above tests, to tested file, is correct.  
Init file is needed in tests folder as relative import is used.
For example:

```python
#test file in tests, testing ..logger.py from shared
#__init__.py file in tests
import pytest
import logging
from ..logger import setup_logger
```

Files from shared import each other with .

```python
#file from shared imports other file form shared
from .logger import log_message
```

Use s flag with pytest to disable output capturing. You will see test oputput if needed.

```bash
pytest -s
```

## ChatGPT Notes

Some of text generated with ai used as a starting point or point.

### Give me simple py, cli app. Help, exit command, loop. Parse input to command [args].

Here is a simple Python CLI app that includes a loop, `help`, `exit` commands, and parses input into commands and arguments:

```python
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
```

#### Features:

-   **Help command**: Displays a list of available commands.
-   **Exit command**: Exits the app when entered.
-   **Command parsing**: Input is split into a command and its associated arguments.

#### Usage:

-   Type `help` for help.
-   Type `exit` to quit the app.
-   Enter any other command followed by arguments, and the app will display the parsed command and arguments.

### I would like that we can add script to command folder and app will know command form file name, description from method and it can dynamically run when input calls for it.

To dynamically load commands from the `commands` folder, you can create a structure that will:

1. **Discover all Python files** in the `commands` folder.
2. **Load the command names** from the filenames and their **descriptions** from a defined method within each command file.
3. **Execute the appropriate function** from the command file based on user input.

Here’s how you can implement this functionality:

#### Updated Project Structure

```plaintext
cli/
├── src/
│   └── cli_app/
│   │   ├── __init__.py
│   │   ├── app.py              # Main CLI logic
│   └── commands/               # Commands folder
│   │   ├── __init__.py         # Empty init file for module
│   │   ├── clear.py            # Clear console command
│   │   ├── example_command.py  # Example dynamic command
```

#### Steps to Implement:

1. **Create a Base Command Structure**
   Each command should be a Python file in the `commands` folder. The command file should include:

    - A function (e.g., `run()`) that gets executed when the command is invoked.
    - A description string that can be accessed dynamically.

2. **Define Command Files in `commands/` Folder**
   Example of `clear.py` (already shown), plus another example command (`example_command.py`):

    **`clear.py`**

    ```python
    # src/commands/clear.py
    import os
    import platform

    def run():
        system = platform.system()
        if system == "Windows":
            os.system('cls')  # Windows command to clear console
        else:
            os.system('clear')  # Unix/Linux/Mac command to clear console

    description = "Clear the console screen"
    ```

    **`example_command.py`**

    ```python
    # src/commands/example_command.py
    def run():
        print("This is an example command!")

    description = "Prints a simple example message"
    ```

3. **Modify `app.py` to Discover and Load Commands Dynamically**

    - **Discover commands dynamically** by scanning the `commands/` folder.
    - **Store command descriptions** and **link to their execution function**.

    ```python
    # src/cli_app/app.py
    import os
    import sys
    import importlib.util

    # Dynamically import all command modules from the 'commands' folder
    def load_commands(commands_folder="src/commands"):
        command_files = []
        for filename in os.listdir(commands_folder):
            if filename.endswith(".py") and filename != "__init__.py":
                command_name = filename[:-3]  # Remove ".py" extension
                command_files.append(command_name)
        return command_files

    def print_help(commands):
        print("Simple CLI App")
        print("Commands:")
        for command in commands:
            print(f"  {command}       - {command['description']}")
        print("  help           - Show this help message")
        print("  exit           - Exit the program")

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

        # Generate a list of command descriptions
        for command_file in command_files:
            module_name = f"commands.{command_file}"
            spec = importlib.util.find_spec(module_name)
            command_module = importlib.import_module(module_name)
            description = getattr(command_module, 'description', 'No description available')
            commands.append({"name": command_file, "description": description})

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

            # Handle dynamic commands
            else:
                command, args = parse_input(user_input)
                if command in [cmd['name'] for cmd in commands]:
                    run_command(command)
                else:
                    print(f"Unknown command '{command}'. Type 'help' for a list of commands.")

    if __name__ == "__main__":
        main()
    ```

#### How It Works:

-   **`load_commands()`** scans the `commands` folder for Python files, excluding `__init__.py`.
-   Each command file (like `clear.py` or `example_command.py`) must include a `run()` function that gets executed when the command is invoked, along with a `description` string that describes the command.
-   **`print_help()`** dynamically lists all available commands and their descriptions.
-   When the user inputs a command, the app will check if it exists in the `commands` folder. If it does, the `run()` function of that command is executed.

#### Example of Usage:

```
> help
Simple CLI App
Commands:
  clear       - Clear the console screen
  example_command - Prints a simple example message
  help        - Show this help message
  exit        - Exit the program

> example_command
This is an example command!

> clear
<Console is cleared>

> exit
Exiting the application.
```

#### How to Add New Commands:

1. Create a new `.py` file in the `src/commands/` folder.
2. Define the `run()` function that implements the command logic.
3. Add a `description` string that describes the command.
4. The new command will be automatically recognized by the app and can be run via CLI.

This allows you to dynamically add new commands to the app by simply placing Python files in the `commands` folder without modifying the main app logic.

###
