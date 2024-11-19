from cli_app.cli_helpers import get_help
from cli_app.config import COMMAND_NAME_MAX_LENGTH

def test_get_help_full():
    folders = {
        "Folder1": {
            "command1": {"description": "Command 1 description"},
            "command2": {"description": "Command 2 description"},
        },
        "Folder2": {
            "command3": {"description": "Command 3 description"},
        }
    }
    selected_folder = "Folder1"
    
    result = get_help(folders, selected_folder)
    
    # Verify the overall structure
    assert "Simple CLI App" in result
    assert "Commands:" in result
    assert "Selected folder: Folder1" in result
    
    # Verify global commands
    assert "help" in result
    assert "exit" in result
    assert "set_folder [folder_name]" in result

    # Verify folder-specific commands
    assert "Folder1 commands:" in result
    assert "command1" in result
    assert "Command 1 description" in result
    assert "command2" in result
    assert "Command 2 description" in result
    assert "Folder2 commands:" in result
    assert "command3" in result
    assert "Command 3 description" in result
    
    # Check for padding correctness
    assert "help" in result and " " * (COMMAND_NAME_MAX_LENGTH - len("help")) in result
    assert "command1" in result and " " * (COMMAND_NAME_MAX_LENGTH - len("command1")) in result

def test_get_help_no_folders():
    folders = {}
    selected_folder = None
    
    result = get_help(folders, selected_folder)
    
    # Verify the overall structure
    assert "Simple CLI App" in result
    assert "Commands:" in result
    assert "Selected folder: None" in result
    
    # Verify global commands
    assert "help" in result
    assert "exit" in result
    assert "set_folder [folder_name]" in result
    
    # No folder-specific commands should be displayed
    assert "commands:" not in result

def test_get_help_no_selected_folder():
    folders = {
        "Folder1": {
            "command1": {"description": "Command 1 description"},
        }
    }
    selected_folder = None
    
    result = get_help(folders, selected_folder)
    
    # Verify the overall structure
    assert "Simple CLI App" in result
    assert "Commands:" in result
    assert "Selected folder: None" in result
    
    # Verify folder-specific commands
    assert "Folder1 commands:" in result
    assert "command1" in result
    assert "Command 1 description" in result

def test_get_help_empty_command_description():
    folders = {
        "Folder1": {
            "command1": {"description": ""},
        }
    }
    selected_folder = "Folder1"
    
    result = get_help(folders, selected_folder)
    
    # Verify the overall structure
    assert "Simple CLI App" in result
    assert "Folder1 commands:" in result
    
    # Verify command with empty description
    assert "command1" in result
    assert "- " in result  # Ensure there is still a dash or placeholder for empty description

def test_get_help_padding():
    folders = {
        "Folder1": {
            "short": {"description": "Short command"},
            "veryverylongcommand": {"description": "A very long command description"},
        }
    }
    selected_folder = "Folder1"
    
    result = get_help(folders, selected_folder)
    
    # Check for padding and alignment correctness
    assert "short" in result
    assert "Short command" in result
    assert "veryverylongcommand" in result
    assert "A very long command description" in result

    # Verify padding exists for each command
    assert "short" in result and " " * (COMMAND_NAME_MAX_LENGTH - len("short")) in result
    assert "veryverylongcommand" in result and " " * (COMMAND_NAME_MAX_LENGTH - len("veryverylongcommand")) in result
