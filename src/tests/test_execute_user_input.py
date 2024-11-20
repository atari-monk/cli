from unittest.mock import patch
from cli_app.command_runner import execute_user_input

# Test case for execute_user_input when a single folder matches
@patch('cli_app.command_runner.parse_input', return_value=('command1', ['arg1']))
@patch('cli_app.command_runner.find_command_in_folders', return_value=['folder1'])
@patch('cli_app.command_runner.run_command')
def test_execute_user_input_single_match(mock_run_command, mock_find_command_in_folders, mock_parse_input):
    folders = {
        'folder1': {'command1': {'arg1': 'value1'}},
        'folder2': {'command2': {'arg2': 'value2'}}
    }
    selected_folder = 'folder1'
    
    # Call the function with a known command that matches exactly one folder
    execute_user_input("command1 arg1", folders, selected_folder)

    # Check that run_command was called with the correct folder and command
    mock_run_command.assert_called_once_with('folder1', 'command1', ['arg1'])

# Test case for execute_user_input when multiple folders match
@patch('cli_app.command_runner.parse_input', return_value=('command1', ['arg1']))
@patch('cli_app.command_runner.find_command_in_folders', return_value=['folder1', 'folder2'])
@patch('cli_app.command_runner.display_menu', return_value='folder1')
@patch('cli_app.command_runner.run_command')
def test_execute_user_input_multiple_matches(mock_run_command, mock_display_menu, mock_find_command_in_folders, mock_parse_input):
    folders = {
        'folder1': {'command1': {'arg1': 'value1'}},
        'folder2': {'command1': {'arg2': 'value2'}}
    }
    selected_folder = 'folder1'
    
    # Call the function with a known command that matches multiple folders
    execute_user_input("command1 arg1", folders, selected_folder)

    # Check that display_menu was called to select a folder from the matching folders
    mock_display_menu.assert_called_once_with(['folder1', 'folder2'])
    
    # Check that run_command was called with the selected folder and command
    mock_run_command.assert_called_once_with('folder1', 'command1', ['arg1'])

# Test case for execute_user_input when no folders match
@patch('cli_app.command_runner.parse_input', return_value=('command3', ['arg1']))
@patch('cli_app.command_runner.find_command_in_folders', return_value=[])
def test_execute_user_input_no_match(mock_find_command_in_folders, mock_parse_input):
    folders = {
        'folder1': {'command1': {'arg1': 'value1'}},
        'folder2': {'command2': {'arg2': 'value2'}}
    }
    selected_folder = 'folder1'
    
    # Call the function with a command that does not exist in any folder
    with patch('builtins.print') as mock_print:
        execute_user_input("command3 arg1", folders, selected_folder)
        
        # Check that the print statement shows the error message
        mock_print.assert_called_once_with("Unknown command 'command3'. Type 'help' for a list of commands.")
