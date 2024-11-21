from unittest.mock import patch
import logging
from cli_app.command_runner import get_valid_choice

logger = logging.getLogger('test_get_valid_choice.py')

# Test valid input scenario
def test_valid_choice():
    options = ['Folder 1', 'Folder 2', 'Folder 3']
    
    with patch('builtins.input', return_value='2'), patch.object(logger, 'info') as mock_info, patch.object(logger, 'error') as mock_error:
        result = get_valid_choice(options)
        assert result == 'Folder 2'
        mock_info.assert_not_called()
        mock_error.assert_not_called()
