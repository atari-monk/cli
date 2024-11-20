import importlib.util
import importlib

def execute_user_input(user_input, folders, selected_folder):

    command, args = parse_input(user_input)

    matching_folders = find_command_in_folders(command)

    if len(matching_folders) == 1:
        selected_folder = matching_folders[0]
        print(f"Automatically selected folder: {selected_folder}")
        run_command(selected_folder, command, args)
    elif len(matching_folders) > 1:
        selected_folder = display_menu(matching_folders)
        run_command(selected_folder, command, args)
    else:
        print(f"Unknown command '{command}'. Type 'help' for a list of commands.")

def parse_input(user_input):
    parts = user_input.split()
    command = parts[0]
    args = parts[1:] if len(parts) > 1 else []
    return command, args

def find_command_in_folders(folders, command_name):
    matches = []
    for folder_name, commands in folders.items():
        if command_name in commands:
            matches.append(folder_name)
    return matches

def run_command(selected_folder, command, args = None):
    module_name = f"{selected_folder}.{command}"
    spec = importlib.util.find_spec(module_name)
    
    if spec is None:
        print(f"Command '{command}' not found.")
        return

    command_module = importlib.import_module(module_name)
    
    if hasattr(command_module, 'run'):
        command_module.run(args)
    else:
        print(f"Command '{command}' does not have a 'run' function.")

def display_menu(options):
        print("Multiple folders contain this command:")
        for i, option in enumerate(options):
            print(f"{i + 1}. {option}")
        while True:
            try:
                choice = int(input("Select a folder by number: ")) - 1
                if 0 <= choice < len(options):
                    return options[choice]
                else:
                    print("Invalid choice. Try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")
