# Cli Helpers

Module providing helper functions.

## generate_string

### Function

Returns text cloned specified amount of times.

```python
def generate_string(count: int, string: str = ' ', max_length: int = 1000) -> str:
    result = string * count
    if len(result) > max_length:
        raise ValueError(f"The resulting string exceeds the maximum allowed length of {max_length}.")
    return result
```

### Examples

```python
# Default behavior with spaces
print(generate_string(5))  # Output: '     ' (5 spaces)

# Custom string
print(generate_string(3, 'test'))  # Output: 'testtesttest'

# Custom max length
print(generate_string(5, 'hello', max_length=20))  # Output: 'hellohellohellohellohello'

# Exceeding max length
try:
    print(generate_string(5, 'longstring', max_length=20))
except ValueError as e:
    print(e)  # Output: "The resulting string exceeds the maximum allowed length of 20."

# Invalid inputs
try:
    print(generate_string(5.5, 'test'))
except TypeError as e:
    print(e)  # Output: "can't multiply sequence by non-int of type 'float'"
```

## generate_padding

### Function

Returns padding for string.  
Fills string with padding, to specified length.

```python
def generate_padding(length: int, string: str) -> str:
    padding_length = length - len(string)
    if padding_length < 0:
        return ''
    return generate_string(padding_length)
```

## get_help

### Function

Returns help/menu for detected commands.

```python
def get_help(folders: dict[str, dict[str, dict[str, str]]], selected_folder: Optional[str]) -> None:
    help = []

    help.append("Simple CLI App")
    help.append("Commands:")

    selected_folder_info = f" Selected folder: {selected_folder}" if selected_folder else " Selected folder: None"
    help.append(f"\n  {selected_folder_info}")

    length = COMMAND_NAME_MAX_LENGTH
    help.append(f"\n  help{generate_padding(length, 'help')}- Show this help message")
    help.append(f"  exit{generate_padding(length, 'exit')}- Exit the program")
    help.append(f"  set_folder [folder_name]{generate_padding(length, 'set_folder')}- Set folder context")

    for folder_name, commands in folders.items():
        help.append(f"\n{folder_name} commands:")
        for command_name, command_info in commands.items():
            help.append(f"  {command_name}{generate_padding(length, command_name)}- {command_info['description']}")

    return "\n".join(help)
```

### Description

The `print_help` function generates a help message for a CLI app, summarizing its available commands and their descriptions. Here's how it works:

**Inputs:**

1. **`folders`**: A nested dictionary structured as `dict[str, dict[str, dict[str, str]]]`.

    - **Outer keys**: Represent folder names.
    - **First inner dictionary**: Maps command names to another dictionary.
    - **Second inner dictionary**: Contains the command's metadata (e.g., description).

    Example:

    ```python
    {
        "folder1": {
            "command1": {"description": "Description of command1"},
            "command2": {"description": "Description of command2"}
        },
        "folder2": {
            "command3": {"description": "Description of command3"}
        }
    }
    ```

2. **`selected_folder`**: A string indicating the currently selected folder, or `None` if no folder is selected.

---

**How It Works:**

1. **Help Header**:

    - The output begins with a title (`"Simple CLI App"`) followed by a list of general commands.

2. **Selected Folder Info**:

    - Includes the name of the currently selected folder if specified, or `"None"` if no folder is selected.

3. **Command Descriptions**:

    - The help text includes:
        - `"help"`: Shows the help message.
        - `"exit"`: Exits the program.
        - `"set_folder [folder_name]"`: Sets the folder context.

4. **Folder-Specific Commands**:

    - Iterates over the `folders` dictionary to append commands grouped by folder names.
    - Each folder section begins with the folder name, followed by its specific commands and descriptions.

5. **Alignment**:

    - Uses `generate_padding` to align command names and their descriptions neatly.

6. **Output**:
    - Returns a formatted string combining all the above information.

---

**Dependencies:**

-   **`generate_padding(length, command_name)`**: Dynamically calculates padding for command names to ensure proper alignment in the help text.
-   **`COMMAND_NAME_MAX_LENGTH`**: Presumably defines the maximum length of a command name for alignment purposes.

---

**Example Output:**
Given the following inputs:

```python
folders = {
    "folder1": {
        "command1": {"description": "Run command1"},
        "command2": {"description": "Run command2"}
    },
    "folder2": {
        "command3": {"description": "Run command3"}
    }
}
selected_folder = "folder1"
COMMAND_NAME_MAX_LENGTH = 15
```

The output might look like:

```
Simple CLI App
Commands:

  Selected folder: folder1

  help           - Show this help message
  exit           - Exit the program
  set_folder [folder_name] - Set folder context

folder1 commands:
  command1       - Run command1
  command2       - Run command2

folder2 commands:
  command3       - Run command3
```

This structure makes it clear and easy for users to understand and navigate the CLI's capabilities.

## get_current_working_directory

### Function

Retrieves the current working directory and returns it as a formatted string.

```python
def get_current_working_directory():
    current_folder = os.getcwd()
    return f"Current working directory: {current_folder}"
```
