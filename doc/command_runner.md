# Command Runner Module

Module responsible for running commands.

## parse_input

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

## ff