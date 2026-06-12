import logging
import os

LOG_FILE = os.path.join(os.path.dirname(__file__), "..", "logs", "trading_bot.log")
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"


def setup_logger() -> logging.Logger:
    logger = logging.getLogger("trading_bot")

    # Guard against duplicate handlers when called multiple times
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    os.makedirs(os.path.dirname(os.path.abspath(LOG_FILE)), exist_ok=True)

    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT))

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
