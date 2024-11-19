import json
from pathlib import Path
import pytest
from unittest.mock import patch, MagicMock
from cli_app.command_loader import load_commands

def test_load_commands_empty_folders():
    result = load_commands([])
    assert result == {}

def test_load_commands_invalid_folder():
    with patch("pathlib.Path.is_dir", return_value=False):
        result = load_commands(['invalid_folder'])
        assert result == {}

def test_load_commands_missing_file():
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = load_commands(['folder1'])
        assert result == {}

def test_load_commands_missing_file_logs_error(caplog):
    with patch("builtins.open", side_effect=FileNotFoundError):
        load_commands(['folder1'])
    
    assert "Error reading descriptions file command_descriptions.json" in caplog.text

def test_load_commands_command_name_too_long():
    descriptions_data = {
        "folder1": {
            "commanddddddddddddddddddddddddddddd": { "description": "Clear the console screen" }
        }
    }

    mock_open = MagicMock()
    mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(descriptions_data)

    mock_rglob = MagicMock()

    mock_subfolder = MagicMock(spec=Path)
    mock_subfolder.stem = "commanddddddddddddddddddddddddddddd"
    mock_subfolder.is_dir.return_value = False
    mock_rglob.return_value = [mock_subfolder]

    with patch("builtins.open", mock_open), patch("pathlib.Path.is_dir", return_value=True), patch("pathlib.Path.rglob", mock_rglob):
        with pytest.raises(ValueError):
            load_commands(['folder1'], descriptions_file='command_descriptions.json')

def test_load_commands_valid_folder():
    mock_subfolder = MagicMock(is_dir=MagicMock(return_value=False))
    mock_subfolder.stem = 'command'
    mock_subfolder.name = 'command.py'

    descriptions_data = {
        "valid_folder": {
            "command": { "description": "Clear the console screen" }
        }
    }

    mock_open = MagicMock()
    mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(descriptions_data)

    mock_rglob = MagicMock()
    mock_rglob.return_value = [mock_subfolder]

    with patch("builtins.open", mock_open), patch("pathlib.Path.is_dir", return_value=True), patch("pathlib.Path.rglob", mock_rglob):
        result = load_commands(['valid_folder'])

    assert 'valid_folder' in result
    assert 'command' in result['valid_folder']
    assert result['valid_folder']['command'] == { "description": "Clear the console screen" }
