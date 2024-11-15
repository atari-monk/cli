import logging

def setup_logger(name, log_file='cli_app.log', level=logging.DEBUG):
    """
    Sets up a shared logger.

    Args:
        name (str): Logger name.
        log_file (str): File to log to.
        level (int): Logging level (default: logging.INFO).

    Returns:
        logging.Logger: Configured logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    if not logger.handlers:  # Avoid adding multiple handlers in recursive imports
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

def log_message(message, logger=None, log_enabled=True):
    """
    Logs a message either using the logger or print, depending on the log_enabled flag.

    Args:
        message (str): The message to log.
        logger (logging.Logger, optional): Logger instance for logging. If None, a default logger is used.
        log_enabled (bool): Flag to toggle logging. If True, logger is used. If False, print is used.
    """
    if log_enabled:
        logger = logger or setup_logger('shared')  # Use injected logger, or fall back to default
        logger.info(message)
    else:
        print(message)
        