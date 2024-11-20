from unittest.mock import MagicMock, patch
from cli_app.command_runner import run_command
import logging

logger = logging.getLogger("cli_app.command_runner")

def test_command_not_found():
    """Test when the specified command module is not found."""
    with patch("importlib.util.find_spec", return_value=None), \
         patch.object(logger, "error") as mock_error_log:
        run_command("commands", "non_existent_command")
        # Check if the logger's error method was called correctly
        mock_error_log.assert_called_once_with(
            "Command 'non_existent_command' not found in folder 'commands'."
        )

def test_command_runs_with_no_arguments():
    """Test when the module has a 'run' function and executes with no arguments."""
    mock_module = MagicMock()
    mock_module.run = MagicMock()
    with patch("importlib.util.find_spec", return_value=True), \
         patch("importlib.import_module", return_value=mock_module), \
         patch.object(logger, "info") as mock_info_log:
        run_command("commands", "valid_command_no_args", args=[])
        mock_info_log.assert_called_once_with(
            "Running command 'valid_command_no_args' with arguments: []"
        )

def test_command_runs_with_arguments():
    """Test when the module has a 'run' function and executes with arguments."""
    mock_module = MagicMock()
    mock_module.run = MagicMock()
    with patch("importlib.util.find_spec", return_value=True), \
         patch("importlib.import_module", return_value=mock_module), \
         patch.object(logger, "info") as mock_info_log:
        run_command("commands", "valid_command_with_args", args=["arg1", "arg2"])
        mock_info_log.assert_called_once_with(
            "Running command 'valid_command_with_args' with arguments: ['arg1', 'arg2']"
        )

def test_command_with_optional_arguments():
    """Test when a command has optional arguments."""
    mock_module = MagicMock()
    mock_module.run = MagicMock()
    
    with patch("importlib.util.find_spec", return_value=True), \
         patch("importlib.import_module", return_value=mock_module), \
         patch.object(logger, "info") as mock_info_log:
        run_command("commands", "command_with_optional_args", args=["optional_arg"])
        mock_info_log.assert_called_once_with("Running command 'command_with_optional_args' with arguments: ['optional_arg']")

def test_multiple_commands_execution():
    """Test running multiple commands sequentially."""
    mock_module = MagicMock()
    mock_module.run = MagicMock()
    
    with patch("importlib.util.find_spec", return_value=True), \
         patch("importlib.import_module", return_value=mock_module), \
         patch.object(logger, "info") as mock_info_log:
        run_command("commands", "command1")
        run_command("commands", "command2")
        
        # Updated the expected log message to reflect actual behavior
        mock_info_log.assert_any_call("Running command 'command1' with arguments: []")
        mock_info_log.assert_any_call("Running command 'command2' with arguments: []")

def test_invalid_command():
    """Test when an invalid command is entered."""
    with patch("importlib.util.find_spec", return_value=None), \
         patch.object(logger, "error") as mock_error_log:  # Change to mock 'error' log
        run_command("commands", "invalid_command")
        
        # Update the expected log message to reflect the actual error log
        mock_error_log.assert_called_once_with("Command 'invalid_command' not found in folder 'commands'.")
