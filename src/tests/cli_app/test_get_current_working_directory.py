import os
from cli_app.cli_helpers import get_current_working_directory

def test_print_current_folder(monkeypatch):
    # Mock the `os.getcwd` method to return a fixed path
    monkeypatch.setattr(os, "getcwd", lambda: "/mocked/path")
    
    # Call the function and assert the result
    result = get_current_working_directory()
    assert result == "Current working directory: /mocked/path"
