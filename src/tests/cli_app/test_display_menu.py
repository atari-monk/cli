import pytest
from unittest.mock import patch
from io import StringIO
import logging
from cli_app.command_runner import display_menu

# Test for display_menu
@pytest.fixture
def mock_input():
    with patch('builtins.input', return_value='1'):
        yield

@pytest.fixture
def mock_logger():
    with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
        # Setting up a custom logger to ensure that it outputs to stderr
        logger = logging.getLogger('cli_app.command_runner')
        logger.setLevel(logging.DEBUG)
        # Remove any existing handlers
        for handler in logger.handlers:
            logger.removeHandler(handler)
        # Add a new stream handler to capture output
        handler = logging.StreamHandler(mock_stderr)
        handler.setLevel(logging.DEBUG)
        logger.addHandler(handler)
        
        yield mock_stderr

def test_display_menu(mock_input, mock_logger):
    options = ['folder1', 'folder2', 'folder3']
    
    # Call the function
    selected_folder = display_menu(options)
    
    # Check that the correct folder was selected
    assert selected_folder == 'folder1'
    
    # Check that the logger output contains the expected info
    log_output = mock_logger.getvalue()
    assert "Multiple folders contain this command:" in log_output
    assert "1. folder1" in log_output
    assert "2. folder2" in log_output
    assert "3. folder3" in log_output
