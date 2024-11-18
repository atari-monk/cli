# Cli_app code

Code with documentation genereted by ai, on my prompts, to add some depth and info.

## discover_folders_with_commands

Code:

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

1. Type annotations

Type annotations in pyton should work with static type checkers mypy or editors/IDEs (e.g., PyCharm, VSCode).  
They are not enforced.  
In new versions of python they are build in and dont require imports.

2. Path

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

3. Method handles case when folder doesn't exist or is inaccessible.

Loggs error, returns empty list.

4. Set comprehension.

```python
ignore_set = {folder.lower() for folder in ignore_these_folders}
```

is using a **set comprehension** to create a set of folder names in lowercase.

**Set Comprehension**:
The `{ ... }` syntax is used for **set comprehensions**, which create a new set by iterating over a sequence and applying some transformation to each element. Sets are collections of unique elements, and they provide fast membership testing using the `in` keyword.

This ensures the function handles folder names consistently, no matter the capitalization of the input or the actual folder names.

5. List comprehension.

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

6. Sorting

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
