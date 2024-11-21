# Logger Documentation

## Overview

This logging system is designed to allow easy configuration and usage of loggers throughout your Python project. It provides both console and file logging with file rotation, ensuring that logs are properly handled and stored. The logger setup supports configuration via a dictionary and allows customization of log levels, log file paths, and formatters.

## Setup Logger

### Function: `setup_logger(name: str, config: Optional[dict[str, Optional[object]]]=None) -> logging.Logger`

This function initializes a logger instance with configurable handlers (console and file). If no configuration is provided, default settings are used.

#### Parameters:

-   `name` (str): The name of the logger. Typically, this will be `__name__`, allowing you to differentiate logs from different modules.
-   `config` (Optional[dict]): A dictionary containing configuration options for the logger. If not provided, default values will be used. The configuration dictionary can contain the following keys:
    -   `'log_file'`: The path to the log file (default: `'logs/app.log'`).
    -   `'log_to_file'`: A boolean indicating if logs should be written to a file (default: `True`).
    -   `'mainLevel'`: The logging level for the main logger filter (default: `logging.DEBUG`).
    -   `'consoleLevel'`: The logging level for the console output (default: `logging.DEBUG`).
    -   `'fileLevel'`: The logging level for the file output (default: `logging.DEBUG`).
    -   `'format'`: The format string for log messages (default: `'%(asctime)s - %(name)s - %(levelname)s - %(message)s'`).
    -   `'max_bytes'`: The maximum size for the log file before it is rotated (default: `10 * 1024 * 1024` or 10MB).
    -   `'backup_count'`: The number of backup log files to keep (default: `3`).

#### Returns:

-   A `logging.Logger` instance configured according to the specified or default configuration.

#### Example Usage:

```python
import logging
from logging_setup import setup_logger

LOGGER_CONFIG = {
    'log_file': 'logs/my_app.log',
    'log_to_file': True,
    'mainLevel': logging.DEBUG,
    'consoleLevel': logging.INFO,
    'fileLevel': logging.DEBUG,
    'format': '%(asctime)s - %(levelname)s - %(message)s',
    'max_bytes': 5 * 1024 * 1024,  # 5 MB max file size
    'backup_count': 5
}

# Initialize the logger
logger = setup_logger(__name__, LOGGER_CONFIG)

# Usage in the module
logger.debug("This is a debug message")
logger.info("This is an info message")
logger.error("This is an error message")
```

### Default Configuration

If no configuration dictionary is passed, the logger will use the following default settings:

```python
{
    'log_file': 'logs/app.log',
    'log_to_file': True,
    'mainLevel': logging.DEBUG,
    'consoleLevel': logging.DEBUG,
    'fileLevel': logging.DEBUG,
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'max_bytes': 10 * 1024 * 1024,  # 10 MB
    'backup_count': 3
}
```

## Logger Usage

Once a logger is created using `setup_logger`, it can be used throughout the module for logging various levels of messages.

### Available Log Levels

-   `logger.debug("Message")`: Logs a message with the debug level. Useful for detailed troubleshooting.
-   `logger.info("Message")`: Logs a message with the info level. This is typically for general information about application flow.
-   `logger.warning("Message")`: Logs a message with the warning level. This is used when something unexpected happens, but it's not an error.
-   `logger.error("Message")`: Logs a message with the error level. This should be used when an error occurs that needs attention.
-   `logger.critical("Message")`: Logs a message with the critical level. This is used for serious errors that may cause the program to terminate.

### Example Usage in a Module:

```python
# In some module, e.g., 'module.py'

from logger import setup_logger
from specific_app.config import LOGGER_CONFIG

# Get logger
logger = setup_logger(__name__, LOGGER_CONFIG)

def my_function():
    logger.info("Starting function execution.")
    try:
        # Some logic
        result = 10 / 0  # This will cause an error
    except ZeroDivisionError:
        logger.error("Attempted to divide by zero.")
    logger.info("Function execution completed.")
```

### Log File Rotation

The log files will rotate once the file size exceeds the limit specified in the `max_bytes` configuration (default is 10MB). The log files will be backed up as specified in the `backup_count` (default is 3 backups). Older log files are preserved with a numerical suffix, e.g., `app.log.1`, `app.log.2`, etc.

### Console Logging

By default, the logger will output log messages to the console with the logging level specified in the `consoleLevel` setting (default is `logging.DEBUG`). This helps to view log messages in real-time during development.

## Notes

-   The logger instance is designed to handle logging in both the console and files simultaneously. You can configure it as per your needs, whether for development or production environments.
-   If you want to use the logger in multiple modules, simply call `setup_logger` in each module and use `logger` for logging. Each module can have its own logger instance, identified by the module's `__name__`.

---
