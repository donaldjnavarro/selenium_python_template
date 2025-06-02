# fixtures/logging_fixture.py

import logging
import os
import sys
from datetime import datetime

__all__ = ['pytest_configure']


class ColoredFormatter(logging.Formatter):
    """Color logs"""
    COLORS = {
        'DEBUG': '\033[94m',   # Blue
        'INFO': '\033[92m',    # Green
        'WARNING': '\033[93m', # Yellow
        'ERROR': '\033[91m',   # Red
        'CRITICAL': '\033[1;91m', # Bold Red
        'DEFAULT': '\033[90m', # Gray (for filename and line number)
        'MESSAGE': '\033[95m', # Purple
        'RESET': '\033[0m',
    }

    def format(self, record):
        super().format(record)
        level_color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        time_color = self.COLORS['DEFAULT']
        file_line_color = self.COLORS['RESET']
        message_colored = f"{level_color}{record.getMessage()}"

        return (
            f"{time_color}[{record.asctime}]"
            f"{level_color}[{record.levelname}]"
            f"{file_line_color}[{record.filename}:{record.lineno}]"
            f" {message_colored}"
            f"{self.COLORS['RESET']}"
        )


def setup_console_logging() -> logging.Handler:
    """Create and return a console handler with colored logs."""
    console_handler = logging.StreamHandler(sys.stdout)
    console_formatter = ColoredFormatter('%(asctime)s', datefmt='%Y-%m-%d %H:%M:%S')
    console_handler.setFormatter(console_formatter)
    return console_handler


def setup_file_logging(log_dir: str = "logs") -> logging.Handler:
    """Create and return a file handler for logs."""
    os.makedirs(log_dir, exist_ok=True)
    log_filename = os.path.join(log_dir, f"pytest_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")
    file_handler = logging.FileHandler(log_filename)
    file_formatter = logging.Formatter(
        fmt='%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    return file_handler


def configure_logging():
    """Configure pytest logging."""
    logger = logging.getLogger()

    # Clear existing handlers to avoid duplicates
    logger.handlers.clear()

    # Add console and file handlers
    logger.addHandler(setup_console_logging())
    logger.addHandler(setup_file_logging())

    # Set global log level
    logger.setLevel(logging.INFO)
