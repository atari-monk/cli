import logging
import os
from typing import Optional
from logging.handlers import RotatingFileHandler

def setup_logger(name: str, config: Optional[dict[str, Optional[object]]]=None) -> logging.Logger:
    if config is None:
        config = {
            'log_file': 'logs/app.log',
            'log_to_file': True,
            'mainLevel': logging.DEBUG,
            'consoleLevel': logging.DEBUG,
            'fileLevel': logging.DEBUG,
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'max_bytes': 10 * 1024 * 1024,  # 10 MB, you can adjust this
            'backup_count': 3,               # Number of backup files to keep
        }

    logger = logging.getLogger(name)
    logger.setLevel(config.get('mainLevel', logging.DEBUG))

    if not logger.hasHandlers():
        # Console handler setup
        console_handler = logging.StreamHandler()
        console_handler.setLevel(config.get('consoleLevel', logging.DEBUG))
        console_formatter = logging.Formatter(config.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        # File handler setup with rotation
        if config.get('log_to_file', True):
            log_file = config.get('log_file', 'logs/app.log')
            if os.path.dirname(log_file):
                os.makedirs(os.path.dirname(log_file), exist_ok=True)
            
            # Rotating file handler setup
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=config.get('max_bytes', 10 * 1024 * 1024),  # Default 10MB
                backupCount=config.get('backup_count', 3)             # Default 5 backups
            )
            file_handler.setLevel(config.get('fileLevel', logging.DEBUG))
            file_formatter = logging.Formatter(config.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)

    return logger
