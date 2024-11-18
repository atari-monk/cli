# Command Loader Module

Module responsible for constructing data on autodetected folders and their commands.  
Code with discusions, to add some depth and info.  
Can be seen as introduction to python.  
Aided by ai, on my prompts, edited.

## discover_folders_with_commands

### Method

Returns list of folders with commands.
For current app folder.  
Ignores specified folders.

```python
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
```

### Type annotations

Type annotations in pyton should work with static type checkers mypy or editors/IDEs (e.g., PyCharm, VSCode).  
They are not enforced.  
In new versions of python they are build in and dont require imports.

### Path

The `Path` class is part of the `pathlib` module, introduced in Python 3.4.  
It provides an object-oriented interface for filesystem path manipulations.  
`Path` can represent file paths, directories, or other filesystem objects.  
You can call methods like `.is_dir()`, `.rglob()`, `.exists()`, etc., directly on the `Path` object.  
`Path` abstracts away differences between operating systems. For example, it handles forward slashes (`/`) and backward slashes (`\`) seamlessly.  
Methods like `.joinpath()`, `.parent`, `.stem`, etc., make filesystem operations more convenient.

**Example Usage**:

```python
src_path = Path(".")  # Represents the current directory
print(src_path.is_dir())  # Checks if it's a directory
print(list(src_path.rglob("*")))  # Recursively lists all files and folders
print(src_path / "subfolder" / "file.txt")  # Combines paths cleanly
```

Method handles case when folder doesn't exist or is inaccessible.
Loggs error, returns empty list.

### Set comprehension.

```python
ignore_set = {folder.lower() for folder in ignore_these_folders}
```

is using a **set comprehension** to create a set of folder names in lowercase.

**Set Comprehension**:
The `{ ... }` syntax is used for **set comprehensions**, which create a new set by iterating over a sequence and applying some transformation to each element. Sets are collections of unique elements, and they provide fast membership testing using the `in` keyword.

This ensures the function handles folder names consistently, no matter the capitalization of the input or the actual folder names.

### List comprehension.

```python
folders = [
    folder.name
    for folder in src_path.rglob("*")  # Recursively searches for all paths
    if folder.is_dir()                # Ensures the path is a directory
    and folder.name.lower() not in ignore_set  # Excludes ignored folders
    and (folder / "__init__.py").exists()  # Checks for the presence of __init__.py
]
```

This block of code uses a **list comprehension** to generate a list of folder names based on specific criteria. Here's a detailed breakdown:

**`src_path.rglob("*")`**:
A method of the `Path` object (`src_path`) from the `pathlib` module.  
Recursively finds all files and directories under the `src_path` directory.  
The `"_"`wildcard matches all names.
Returns an iterator of`Path` objects for every file and folder it encounters.

**`folder.is_dir()`**:
Ensures that only directories are included in the list comprehension.
Filters out files and symbolic links.

**`folder.name.lower() not in ignore_set`**:
Checks if the lowercase name of the current folder (`folder.name.lower()`) is **not** in the set of ignored folder names (`ignore_set`).
This makes the exclusion of folders case-insensitive and prevents processing of unwanted directories.

**`(folder / "__init__.py").exists()`**:
This checks whether the directory contains a file named `__init__.py`.
The syntax `(folder / "__init__.py")` creates a new `Path` object by appending `"__init__.py"` to the current folder's path.
**`exists()`** ensures the file actually exists on the filesystem.
This is commonly used to identify Python packages, as `__init__.py` is a marker for package directories.

**`folder.name`**:
Extracts the **name** of the folder (not the full path) using the `.name` attribute of the `Path` object.

**Result**:
Creates a list (`folders`) containing the names of directories under `src_path` that:

1.  Are not in the ignore list.
2.  Contain an `__init__.py` file.

The process is case-insensitive and efficient with concise filtering.

### Sorting

```python
sorted(folders)
```

takes the `folders` list and returns a new list that is **sorted in ascending order**.

**`sorted()` Function**:
The built-in Python function `sorted()` sorts the elements of an iterable (like a list) and returns a new list.
By default, it sorts in **ascending order** (lexicographical for strings).

**Why Use `sorted()`?**
Sorting ensures that the output is predictable and consistent, which can be helpful for:

-   Debugging (easy to read logs).
-   Downstream processing (like alphabetized UI elements or ordered iteration).

**Customization**:
You can provide a custom sorting key using the `key` parameter:

```python
sorted(folders, key=str.lower)  # Case-insensitive sorting
```

**Reverse Order**:
To sort in descending order, use the `reverse=True` parameter:

```python
sorted(folders, reverse=True)
```

**In-Place Sorting**:
If you don't need a new list but want to sort the original list in place, use `.sort()`:

```python
folders.sort()
```

## load_commands

### Method

Takes list of folders with commands, returns dictionary that contains folder's command list.

```python
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
```

### Enforcing type at runtime

Checking argument type and raising error if it is not as expected.

```python
 if not isinstance(folders, list):
        raise TypeError("The 'folders' parameter must be a list of folder names.")
```

### Dictionary

`folder_commands = {}` defines an **empty dictionary** in Python.

A dictionary in Python is a data structure that stores key-value pairs. It's similar to a hash map or associative array in other programming languages.

```python
# Define an empty dictionary
folder_commands = {}

# Add key-value pairs to the dictionary
folder_commands["create"] = "Create a new folder"
folder_commands["delete"] = "Delete an existing folder"

# Access a value by key
print(folder_commands["create"])  # Output: Create a new folder

# Check if a key exists
if "delete" in folder_commands:
    print("Delete command is available.")

# Loop through the dictionary
for command, description in folder_commands.items():
    print(f"{command}: {description}")
```

Characteristics:
**Keys**:
Must be immutable (e.g., strings, numbers, or tuples).  
Must be unique.

**Values**:
Can be any data type (e.g., strings, lists, objects).

**Dynamic**:
You can add, update, or delete key-value pairs dynamically.

Common Operations:
=**Adding/Updating a Key**: `folder_commands["key"] = value`  
**Deleting a Key**: `del folder_commands["key"]`  
**Retrieving a Value**: `folder_commands["key"]`  
**Iterating**: `for key, value in folder_commands.items():`

### List

A **list** in Python is a mutable, ordered collection of items. It allows you to store multiple elements in a single variable and supports various data types, including integers, strings, floats, and even other lists or objects.

Key Characteristics of Python Lists:

1. **Ordered**: The order of items is maintained. Each element has an index starting from 0.
2. **Mutable**: Lists can be modified after creation (e.g., items can be added, removed, or changed).
3. **Heterogeneous**: A list can hold elements of different data types.
    ```python
    mixed_list = [1, "apple", 3.14, True]
    ```

Creating a List:

-   Empty list: `my_list = []`
-   With elements: `my_list = [1, 2, 3]`

Accessing Elements:

-   By index: `my_list[0]` (first element)
-   Negative indexing: `my_list[-1]` (last element)

Common Operations:

1. **Add Items**:

    - Append to the end: `my_list.append(item)`
    - Insert at an index: `my_list.insert(index, item)`

2. **Remove Items**:

    - By value: `my_list.remove(item)`
    - By index: `del my_list[index]` or `my_list.pop(index)`

3. **Iterate**:

    ```python
    for item in my_list:
        print(item)
    ```

4. **Check Membership**:

    ```python
    if "apple" in my_list:
        print("Found!")
    ```

5. **Slice**:
    ```python
    sub_list = my_list[1:3]  # Gets items at index 1 and 2
    ```

Example:

```python
fruits = ["apple", "banana", "cherry"]
fruits.append("orange")  # ['apple', 'banana', 'cherry', 'orange']
fruits.remove("banana")  # ['apple', 'cherry', 'orange']
print(fruits[1])         # 'cherry'
```

Useful Methods:

-   `len(my_list)`: Get the number of items.
-   `my_list.sort()`: Sort the list (in-place).
-   `my_list.reverse()`: Reverse the order (in-place).

## generate_command_descriptions

### Method

Loads descriptions for commands.

```python
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
```

### Read Json

```python
try:
        with open(descriptions_file, 'r') as f:
            descriptions_data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        logger.error(f"Error reading descriptions file {descriptions_file}: {e}")
        return []
```

Tries to read and parse a JSON file and logs any errors if they arise, returning an empty list in case of failure.

