import pytest
import logging
from ..logger import setup_logger

@pytest.fixture
def logger(tmp_path):
    # Use a temporary file for logging during the test
    log_file = tmp_path / "test.log"
    return setup_logger('test_logger', str(log_file), logging.DEBUG)

def test_logger_logs_to_file(logger, tmp_path):
    logger.debug('This is a debug message')

    # Check if the message is written to the temporary log file
    log_file = tmp_path / "test.log"
    with open(log_file, 'r') as file:
        log_contents = file.read()

    # Print log contents to the console
    print("Log file contents:\n", log_contents)

    # Assert the message is in the log file contents
    assert 'This is a debug message' in log_contents
