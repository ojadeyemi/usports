"""Logger configurations"""

import logging
import os


def setup_logging():
    """Sets up logging configurations."""
    log_level = os.getenv("LOG_LEVEL", "INFO")  # Default to INFO if LOG_LEVEL is not set

    if log_level == "DEBUG":
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(message)s"
    else:
        log_format = "%(message)s"

    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=[
            logging.StreamHandler(),  # Output logs to the console
        ],
        datefmt="%d/%m/%Y %H:%M:%S",
    )
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("hpack").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)
    logger = logging.getLogger(__name__)

    return logger
