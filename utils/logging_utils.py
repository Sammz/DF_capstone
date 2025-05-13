from pathlib import Path
from decimal import Decimal
import logging


def setup_logger(name, log_file, level=logging.DEBUG, base_path=None):
    """Function to setup a logger; can be used in multiple modules."""
    # Ensure the logs directory exists
    project_root = Path(base_path or __file__).resolve().parent.parent
    log_directory = project_root / 'logs'
    log_directory.mkdir(parents=True, exist_ok=True)

    # Create a logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create file handler
    file_handler = logging.FileHandler(log_directory / log_file)
    file_handler.setLevel(level)

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    # Create formatter and add it to the handlers
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger


def log_extract_success(logger, type, shape, execution_time, expected_rate):
    logger.setLevel(logging.INFO)
    logger.info(f"Data extraction successful for {type}!")
    logger.info(f"Extracted {shape[0]} rows " f"and {shape[1]} columns")
    logger.info(f"Execution time: {round(execution_time, 3)} seconds")

    # Uses decimal function to ensure actual_rate is printed in
    # decimal format instead of scientific format
    actual_rate = round(Decimal(execution_time / shape[0]), 5)

    if actual_rate <= expected_rate:
        logger.info(
            "Execution time per row: " f"{actual_rate} seconds"
        )
    else:
        logger.setLevel(logging.WARNING)
        logger.warning(
            f"Execution time per row exceeds {expected_rate}: "
            f"{actual_rate} seconds"
        )
