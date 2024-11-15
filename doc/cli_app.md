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
test.log
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
