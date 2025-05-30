import logging
from logging.handlers import RotatingFileHandler

class AppLogger:
    def __init__(self):
        self.logger = logging.getLogger('bookinn_api')
        self.setup_logger()

    def setup_logger(self):
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # File handler for all logs
        # file_handler = RotatingFileHandler(
        #     'logs/general/app.log',
        #     maxBytes=1024 * 1024,
        #     backupCount=5
        # )
        # file_handler.setFormatter(formatter)
        # file_handler.setLevel(logging.INFO)
        #
        # # Error logs handler
        # error_handler = RotatingFileHandler(
        #     'logs/errors/error.log',
        #     maxBytes=1024*1024,
        #     backupCount=5
        # )
        # error_handler.setFormatter(formatter)
        # error_handler.setLevel(logging.ERROR)

        # Security-related logs handler
        # security_handler = RotatingFileHandler(
        #     'logs/security/security.log',
        #     maxBytes=1024*1024,
        #     backupCount=5
        # )
        # security_handler.setFormatter(formatter)
        # security_handler.setLevel(logging.ERROR)
        
        # Development console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.DEBUG)
        
        # self.logger.addHandler(file_handler)
        # self.logger.addHandler(error_handler)
        self.logger.addHandler(console_handler)
        self.logger.setLevel(logging.INFO)


logger = AppLogger().logger
