import datetime
import logging

logger = logging.getLogger()

formatter = logging.Formatter(
    fmt="%(asctime)s - %(levelname)s - %(message)s"
)


file_handler = logging.FileHandler(f"logs/app.log")
file_handler.setFormatter(formatter)

logger.handlers = [file_handler]

logger.setLevel(logging.INFO)
