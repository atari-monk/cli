import os
from .logger import log_message

def ensure_folder_exists(folder_path, logger=None, log_enabled=True):
    """
    Checks if a folder exists, and creates it if it doesn't.

    Args:
        folder_path (str): Path to the folder.
        logger (logging.Logger, optional): Logger instance for logging. If None, a default logger is used.
        log_enabled (bool): Flag to toggle logging. If True, logger is used. If False, print is used.
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        log_message(f"Folder created: {folder_path}", logger, log_enabled)
    else:
        log_message(f"Folder already exists: {folder_path}", logger, log_enabled)
