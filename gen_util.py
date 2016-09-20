import sys
import logging, logging.handlers

class LoggingUtil(object):
    def __init__(self, log_file_name, level=logging.INFO):
        self.logger = self._create_logger(log_file_name, level)

    def _create_logger(self, log_file_name, level=logging.INFO):
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        logger = logging.getLogger(__name__)
        logger.setLevel(level)
        file_handler = logging.handlers.RotatingFileHandler(log_file_name, mode='a', maxBytes=500000, backupCount=7)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        std_handler = logging.StreamHandler(sys.stdout)
        std_handler.setFormatter(formatter)
        logger.addHandler(std_handler)
        return logger

    def _log_msg(self, level, value):
        if level == logging.DEBUG:
            self.logger.debug(value)
        elif level == logging.WARNING:
            self.logger.warning(value)
        elif level == logging.ERROR:
            self.logger.error(value)
        else:
            self.logger.info(value)

    def debug(self, value):
        self._log_msg(logging.DEBUG, value)

    def info(self, value):
        self._log_msg(logging.INFO, value)

    def warning(self, value):
        self._log_msg(logging.WARNING, value)

    def error(self, value):
        self._log_msg(logging.ERROR, value)


