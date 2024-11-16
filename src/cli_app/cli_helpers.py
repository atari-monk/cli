from cli_app.command_loader import COMMAND_NAME_MAX_LENGTH

def generate_spaces(count):
    """
    Generates a string with the specified number of spaces.

    Args:
        count (int): The number of spaces to generate.

    Returns:
        str: A string containing 'count' spaces.
    """
    if count < 0:
        raise ValueError("Count must be a non-negative integer.")
    return ' ' * count

def print_help(commands):
    print("Simple CLI App")
    print("Commands:")
    lenght = COMMAND_NAME_MAX_LENGTH
    for command in commands:
        print(f"  {command['name']}{generate_spaces(lenght - len(command['name']))}- {command['description']}")
    print(f"  help{generate_spaces(lenght - len('help'))}- Show this help message")
    print(f"  exit{generate_spaces(lenght - len('exit'))}- Exit the program")