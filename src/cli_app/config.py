import logging

COMMAND_NAME_MAX_LENGTH = 20
LOGGER_CONFIG = {
            'log_file': 'logs/cli_app.log',
            'log_to_file': True,
            'mainLevel': logging.DEBUG,
            'consoleLevel': logging.DEBUG,
            'fileLevel': logging.DEBUG,
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'max_bytes': 10 * 1024 * 1024,  # 10 MB, you can adjust this
            'backup_count': 3, 
        }