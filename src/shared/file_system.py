import logging
import os
from .logger import setup_logger

setup_logger(__name__)
logger = logging.getLogger(__name__)

def ensure_folder_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        logger.info(f"Folder created: {folder_path}")
    else:
        logger.info(f"Folder already exists: {folder_path}")
