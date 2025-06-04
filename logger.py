"""
Logging configuration for the application.
"""
import os
import sys
import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler
from typing import Optional

from config import LOG_LEVEL, CONSOLE_LOGGING, FILE_LOGGING

# ANSI color codes
COLORS = {
    'DEBUG': '\033[36m',    # Cyan
    'INFO': '\033[32m',     # Green
    'WARNING': '\033[33m',  # Yellow
    'ERROR': '\033[31m',    # Red
    'CRITICAL': '\033[41m', # Red background
    'RESET': '\033[0m'      # Reset color
}

class ColoredFormatter(logging.Formatter):
    """Custom formatter that adds colors to log levels."""

    def format(self, record):
        # Add colors if we're outputting to a terminal
        if sys.stdout.isatty():
            record.levelname = (
                f"{COLORS.get(record.levelname, '')}"
                f"{record.levelname}"
                f"{COLORS['RESET']}"
            )
        return super().format(record)

# Create logs directory if file logging is enabled
LOGS_DIR = "logs"
if FILE_LOGGING:
    os.makedirs(LOGS_DIR, exist_ok=True)

def setup_logger(name: str) -> Optional[logging.Logger]:
    """
    Set up a logger with optional file and console handlers.

    Args:
        name: Name of the logger

    Returns:
        Configured logger instance or None if all logging is disabled
    """
    if not (CONSOLE_LOGGING or FILE_LOGGING):
        return None

    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)

    # Remove any existing handlers
    logger.handlers = []

    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_formatter = ColoredFormatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # File handler (rotating log files)
    if FILE_LOGGING:
        log_file = os.path.join(LOGS_DIR, f"{name}.log")
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(LOG_LEVEL)
        logger.addHandler(file_handler)

    # Console handler
    if CONSOLE_LOGGING:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(LOG_LEVEL)
        logger.addHandler(console_handler)

    return logger

# Create loggers
app_logger = setup_logger('app')
api_logger = setup_logger('api')

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger by name. If logging is disabled, return a dummy logger.

    Args:
        name: Name of the logger

    Returns:
        Logger instance that will either log or do nothing
    """
    if not (CONSOLE_LOGGING or FILE_LOGGING):
        return logging.getLogger('dummy')
    return logging.getLogger(name)
