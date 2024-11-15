import pytest
import os
from unittest.mock import MagicMock
from ..file_system import ensure_folder_exists

@pytest.fixture
def mock_logger():
    # Create a mock logger to pass into the function
    return MagicMock()

def test_ensure_folder_exists_create_folder(mock_logger, caplog):
    folder_path = "test_folder"
    
    # Run the function with log_enabled=True
    ensure_folder_exists(folder_path, logger=mock_logger, log_enabled=True)

    # Assert the folder was created and the logger received the expected call
    assert os.path.exists(folder_path)
    mock_logger.info.assert_called_with(f"Folder created: {folder_path}")
    
    # Clean up
    os.rmdir(folder_path)

def test_ensure_folder_exists_folder_exists(mock_logger, caplog):
    folder_path = "test_folder"
    
    # Create the folder first
    os.makedirs(folder_path)

    # Run the function with log_enabled=True
    ensure_folder_exists(folder_path, logger=mock_logger, log_enabled=True)

    # Assert the logger was called with the message that the folder already exists
    mock_logger.info.assert_called_with(f"Folder already exists: {folder_path}")
    
    # Clean up
    os.rmdir(folder_path)

def test_ensure_folder_exists_without_logging(mock_logger, caplog):
    folder_path = "test_folder"
    
    # Run the function with log_enabled=False
    ensure_folder_exists(folder_path, logger=mock_logger, log_enabled=False)

    # Check if no log message was generated
    assert len(caplog.records) == 0

    # Clean up
    os.rmdir(folder_path)
