# **Command Runner Module**

Module responsible for running commands.

## **parse_input**

### Function

Parses a user's input string into a command and a list of arguments, supporting quoted strings for multi-word arguments.

```python
def parse_input(user_input: str) -> tuple[str, list[str]]:
    if not user_input.strip():
        return '', []

    parts = shlex.split(user_input)
    command = parts[0]
    args = parts[1:]
    return command, args
```

### Type Annotations

Type annotations in Python should work with static type checkers like `mypy` or IDEs (e.g., PyCharm, VSCode).  
They are not enforced but help ensure consistency.  
Modern Python supports type annotations natively (e.g., `str`, `list`, `tuple`).

### `shlex.split`

The `shlex.split` function is part of Python's `shlex` module. It provides shell-like splitting, respecting quoted strings as single entities.

**Why use `shlex.split`:**

-   It handles quoted strings (e.g., `"multi-word argument"`) correctly.
-   Supports escape sequences like `\"` for embedding quotes within strings.
-   It simplifies the implementation, avoiding manual parsing logic.

**Example Usage:**

```python
import shlex

# Splits respecting quoted arguments
parts = shlex.split('command "arg with spaces" arg2')
print(parts)  # Output: ['command', 'arg with spaces', 'arg2']
```

### Empty Input Handling

If the input string is empty or contains only whitespace, the method:

1. Logs the error (optional).
2. Returns an empty command and argument list: `("", [])`.

### Returns

Returns a tuple where:

-   The first element is the command (a string).
-   The second element is a list of arguments, which can include multi-word arguments if quoted.

### Example Usage

**Basic Example:**

```python
print(parse_input("command arg1 arg2"))
# Output: ('command', ['arg1', 'arg2'])
```

**Handling Quoted Strings:**

```python
print(parse_input('command "arg with spaces" arg2'))
# Output: ('command', ['arg with spaces', 'arg2'])
```

**Edge Case (Empty Input):**

```python
print(parse_input(""))
# Output: ('', [])
```

### Robustness

-   Handles empty strings or whitespace gracefully.
-   Supports complex input with mixed quotes, escape characters, and special symbols.
-   Provides a clear and reliable mechanism for parsing user input in command-line interfaces or similar applications.

### Example with Edge Cases

```python
# Single-word command
assert parse_input("run") == ("run", [])

# Command with quoted multi-word arguments
assert parse_input('run "multi word argument"') == ("run", ["multi word argument"])

# Command with escaped quotes
assert parse_input('run "arg with \\"embedded quotes\\""') == ("run", ['arg with "embedded quotes"'])
```

## **find_command_in_folders**

### Function

Searches for a specific command name in the folders and returns a list of folder names that contain the command.

```python
def find_command_in_folders(
    folders: Dict[str, Dict[str, Dict[str, str]]],
    command_name: str
) -> List[str]:
```

### Parameters

-   **folders** (`Dict[str, Dict[str, Dict[str, str]]]`):
    A dictionary representing the folder structure, where:

    -   Keys are folder names (`str`).
    -   Values are dictionaries where each key is a command name (`str`), and the value is a dictionary of command details (e.g., description).

    Example:

    ```python
    {
        "commands": {
            "clear": { "description": "Clear the console screen" },
            "example": { "description": "Prints a simple example message" }
        },
        "log_project": {
            "example": { "description": "Prints a simple example message from log project" }
        }
    }
    ```

-   **command_name** (`str`):
    A string representing the name of the command to search for.

### Returns

-   **List[str]**:
    A list of folder names (`str`) where the specified `command_name` is found in the folder's commands. If the command is not found in any folder, an empty list is returned.

### Example

```python
folders = {
    "commands": {
        "clear": { "description": "Clear the console screen" },
        "example": { "description": "Prints a simple example message" }
    },
    "log_project": {
        "example": { "description": "Prints a simple example message from log project" }
    },
    "misc_project": {
        "clear": { "description": "Clears something in the misc project" }
    },
    "empty_project": {}
}

result = find_command_in_folders(folders, "example")
# result: ['commands', 'log_project']
```

### Explanation

-   The function searches through the provided `folders` dictionary for a given `command_name`.
-   It returns a list of all folders where the `command_name` exists as a key in the respective folder's commands.
-   If the command is not found in any folder, the result will be an empty list.

## **run_command**

### **Function**

Dynamically imports and executes a command module's `run` function with optional arguments.

```python
def run_command(selected_folder: str, command: str, args: Optional[list[str]] = None) -> None:
    args = args or []

    module_name = f"{selected_folder}.{command}"
    logger.debug(f"Attempting to find module: {module_name}")

    spec = importlib.util.find_spec(module_name)
    if spec is None:
        logger.error(f"Command '{command}' not found in folder '{selected_folder}'.")
        return

    try:
        command_module = importlib.import_module(module_name)
    except Exception as e:
        logger.exception(f"Failed to import module '{module_name}'. Error: {e}")
        return

    if hasattr(command_module, 'run'):
        try:
            logger.info(f"Running command '{command}' with arguments: {args}")
            command_module.run(args)
        except Exception as e:
            logger.exception(f"An error occurred while executing the 'run' function in '{module_name}'. Error: {e}")
    else:
        logger.warning(f"Command '{command}' does not have a 'run' function.")
```

### **Parameters**

-   **`selected_folder`** (`str`):  
    The name of the folder containing the command module.  
    Example: `"commands"`.

-   **`command`** (`str`):  
    The name of the command module to execute.  
    Example: `"example"`.

-   **`args`** (`Optional[List[str]]`):  
    A list of arguments to pass to the `run` function.  
    If no arguments are provided, this defaults to an empty list (`[]`).  
    Example: `["arg1", "arg2"]`.

### **Returns**

-   **`None`**:  
    The function performs its operations but does not return any value.

### **Type Annotations**

-   **`Optional[List[str]]`**:
    -   Indicates that `args` can either be a list of strings or `None`.
    -   If `None`, the function will default to an empty list.
    -   Equivalent to `List[str] | None` in Python 3.10 or later.

### **Logging**

The function uses the `logging` module to provide detailed output at various stages:

-   **DEBUG**: Logs information about the module being searched for.
-   **ERROR**: Logs when the command or folder is not found or cannot be imported.
-   **WARNING**: Logs when the `run` function is missing in the imported module.
-   **INFO**: Logs successful execution of the `run` function.

### **Error Handling**

1. Handles missing modules gracefully:
    - Logs an error if the module is not found.
2. Handles import errors:
    - Logs exceptions during module import.
3. Handles missing `run` function:
    - Logs a warning if the `run` function is not present in the imported module.
4. Handles runtime errors:
    - Logs any exceptions raised during the execution of the `run` function.

### **Example Usage**

#### **Example 1: Running a command**

```python
import logging

logging.basicConfig(level=logging.DEBUG)

# Run the "example" command from the "commands" folder with two arguments
run_command("commands", "example", ["arg1", "arg2"])
```

#### **Example 2: Missing command**

```python
# Run a non-existent command
run_command("commands", "non_existent_command")
# Logs: ERROR: Command 'non_existent_command' not found in folder 'commands'.
```

#### **Example 3: Missing `run` function**

```python
# Logs: WARNING: Command 'example' does not have a 'run' function.
run_command("commands", "example_without_run")
```

---

### **Notes**

1. **Dynamic Imports**:
    - Uses `importlib.util.find_spec` and `importlib.import_module` for dynamic loading of modules.
2. **Logging Configuration**:
    - Ensure logging is configured in your application to view logs produced by the function.

---

### **Path**

-   `importlib` module:
    -   Part of Python’s standard library.
    -   Used here for dynamically finding and importing command modules.
    -   Functions:
        -   `importlib.util.find_spec`: Finds the specification for a module.
        -   `importlib.import_module`: Dynamically imports a module.

---

### **Potential Enhancements**

-   Add support for specifying fallback commands.
-   Enable returning results from the `run` function if needed.

## **display_menu**

### **Function**

Displays a menu with the provided folder options and prompts the user to select one.

```python
def display_menu(options: list[str]) -> str:
    logger.info("Multiple folders contain this command:")
    for index, option in enumerate(options, start=1):
        logger.info(f"{index}. {option}")
```

### **Parameters**

-   **`options`** (`List[str]`):  
     A list of folder names to display as options.  
     Example: `["folder1", "folder2", "folder3"]`.

### **Returns**

-   **`str`**:  
     The name of the folder selected by the user.

### **Explanation**

The function shows a numbered list of options to the user and calls a helper function (`get_valid_choice`) to handle the user input. It ensures that the user's input is valid and returns the selected folder.

### **Example Usage**

```python
folders = ["folder1", "folder2", "folder3"]
selected_folder = display_menu(folders)
print(f"You selected: {selected_folder}")
```

---

## **get_valid_choice**

### **Function**

Prompts the user to select a valid folder from the list of options.

```python
def get_valid_choice(options: list[str]) -> str:
    while True:
        try:
            choice = int(input("Select a folder by number: ")) - 1
            if 0 <= choice < len(options):
                return options[choice]
            else:
                logger.info("Invalid choice. Please choose a number between 1 and", len(options))
        except ValueError:
            logger.error("Invalid input. Please enter a valid number.")
```

### **Parameters**

-   **`options`** (`List[str]`):  
     A list of folder names to choose from.  
     Example: `["folder1", "folder2", "folder3"]`.

### **Returns**

-   **`str`**:  
     The folder name that the user selects.

### **Explanation**

This helper function handles the logic of validating user input. It will continue prompting the user until they select a valid folder from the provided list. If the input is invalid, it will display an error message.

### **Example Usage**

```python
folders = ["folder1", "folder2", "folder3"]
selected_folder = get_valid_choice(folders)
print(f"You selected: {selected_folder}")
```

---

### **Notes**

-   **Error Handling**:

    -   If the user inputs an invalid value (e.g., a string instead of a number), the function will prompt them again.
    -   If the input number is out of range, the function will inform the user and ask again.

-   **User-Friendly**:
    -   The function logs helpful error messages to guide the user in case of invalid input.
    -   The user can select folders by their displayed number in the list.

---

Here is the documentation for the `execute_user_input` function:

---

## **execute_user_input**

Handles user input by parsing the command, identifying the corresponding folder(s), and executing the command. The function manages three cases:

1. When a single folder matches the command.
2. When multiple folders match, prompting the user to select one.
3. When no folders match, displaying an error message.

### Parameters:

-   **`user_input`** (`str`): The raw user input string containing the command and arguments.
-   **`folders`** (`dict[str, dict[str, dict[str, str]]]`): A dictionary representing folders and their contents. The keys are folder names, and the values are dictionaries representing commands and their arguments.
-   **`selected_folder`** (`str`): The current folder selected by the user or default folder. This will be updated based on the command matching logic.

### Returns:

-   **None**: The function does not return a value. Instead, it either runs the command, displays a menu, or shows an error message based on the input.

### Behavior:

1. **Single Match**:
    - If exactly one folder contains the given command, it is automatically selected, and the command is executed for that folder.
2. **Multiple Matches**:
    - If more than one folder contains the command, the user is prompted to select from a list of matching folders using a menu system.
3. **No Match**:
    - If no folders contain the command, an error message is displayed informing the user that the command is unknown.

### Example:

```python
folders = {
    'folder1': {'command1': {'arg1': 'value1'}},
    'folder2': {'command1': {'arg1': 'value2'}},
    'folder3': {'command2': {'arg1': 'value3'}}
}

# User input for a known command in multiple folders
execute_user_input("command1 arg1", folders, 'folder1')
```

In this example:

-   Since `command1` exists in both `folder1` and `folder2`, the user will be presented with a menu to choose between these two folders.

```python
# User input for an unknown command
execute_user_input("unknown_command", folders, 'folder1')
```

In this case:

-   The function will print: `"Unknown command 'unknown_command'. Type 'help' for a list of commands."`

#### Notes:

-   The function relies on external functions (`parse_input`, `find_command_in_folders`, `display_menu`, and `run_command`) to perform parsing, finding matching folders, displaying the menu, and running the commands respectively.
-   The `selected_folder` is updated based on the user's input or the automatic selection process.

---
