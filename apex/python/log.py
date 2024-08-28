import logging
import os

CUSTOM_LOGGING_LEVEL = 60
CUSTOM_LOGGING_LEVEL_NAME = 'PRODUCTION'
logging.addLevelName(CUSTOM_LOGGING_LEVEL, CUSTOM_LOGGING_LEVEL_NAME)

class Logger:
    def __init__(self, name:str, level = CUSTOM_LOGGING_LEVEL):
        self.string = name
        self._logger = logging.getLogger(name)

        #Set the logging level for filtering logging information
        self._logger.setLevel(level=level)

        #Create the log file if it doesn't exist already.
        log_file_path = os.path.join("../logging", f"{name}.log")
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

        #Create a file handle to dump the log contents.
        file_handle = logging.FileHandler(log_file_path, mode="w")
        file_handle.setLevel(level=level)
        file_handle_format = logging.Formatter(fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt='%Y-%m-%d %H:%M:%S')
        file_handle.setFormatter(file_handle_format)
        self._logger.addHandler(file_handle)

        self.log_info(f"Starting to record {name} events in apex/python/logging/{name}.log")

    def log_info(self, name:str) ->None:
        self._logger.info("%s", name)

    def log_warning(self, name:str)->None:
        self._logger.warning("%s", name)

    def log_error(self, name:str)->None:
        self._logger.error("%s", name)

    def log_critical(self, name:str)->None:
        self._logger.critical("%s", name)