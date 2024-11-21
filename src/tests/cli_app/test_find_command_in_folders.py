import pytest
from typing import Dict
from cli_app.command_runner import find_command_in_folders

@pytest.fixture
def sample_folders() -> Dict[str, Dict[str, Dict[str, str]]]:
    return {
        "commands": {
            "clear": { "description": "Clear the console screen" },
            "example": { "description": "Prints a simple example message" }
        },
        "log_project": {
            "example": { "description": "Prints a simple example message from log project" }
        },
        "misc_project": {
            "clear": { "description": "Clears something in the misc project" }
        },
        "empty_project": {}
    }

def test_find_command_in_folders_existing_command(sample_folders):
    # Test searching for a command that exists in multiple folders
    result = find_command_in_folders(sample_folders, "example")
    assert result == ["commands", "log_project"], "Should return folders containing 'example' command"

def test_find_command_in_folders_single_match(sample_folders):
    # Test searching for a command that exists in one folder
    result = find_command_in_folders(sample_folders, "clear")
    assert result == ["commands", "misc_project"], "Should return folders containing 'clear' command"

def test_find_command_in_folders_no_match(sample_folders):
    # Test searching for a command that doesn't exist in any folder
    result = find_command_in_folders(sample_folders, "non_existent_command")
    assert result == [], "Should return an empty list when command is not found"

def test_find_command_in_folders_empty_folders(sample_folders):
    # Test searching in an empty folder
    result = find_command_in_folders(sample_folders, "example")
    assert result == ["commands", "log_project"], "Should still work when some folders have no commands"

def test_find_command_in_folders_case_sensitivity(sample_folders):
    # Test searching for a command with case sensitivity
    result = find_command_in_folders(sample_folders, "Example")
    assert result == [], "Should return an empty list as 'Example' is case-sensitive"
