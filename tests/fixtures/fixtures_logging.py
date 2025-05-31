"""Fixtures for handling logging"""

# Standard imports
from __future__ import annotations

__all__ = ['pytest_configure']  # Public fixture

import logging
import sys

# Define your custom formatter class for colorized logs and file info
class ColoredFormatter(logging.Formatter):
    """Color logs"""
    
    # Define color codes for different parts of the log
    COLORS = {
        'DEBUG': '\033[94m',   # Blue
        'INFO': '\033[92m',    # Green
        'WARNING': '\033[93m', # Yellow
        'ERROR': '\033[91m',   # Red
        'CRITICAL': '\033[1;91m', # Bold Red
        'DEFAULT': '\033[90m', # Gray (for filename and line number)
        'MESSAGE': '\033[95m', # Purple (for log message)
        'RESET': '\033[0m',    # Reset to default color
    }

    def format(self, record):
        """Format with colors and useful details."""
        super().format(record)

        level_color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        level_colored = (
            f"{level_color}"
            f"[{record.levelname}]"
        )

        time_color = self.COLORS['DEFAULT']
        time_colored = f"{time_color}[{record.asctime}]"

        file_line_color = self.COLORS['RESET']
        file_line_colored = (
            f"{file_line_color}"
            f"[{record.filename}:{record.lineno}]"
        )

        message_colored = (
            f"{level_color}"
            f"{record.getMessage()}"
        )

        formatted_message = (
            f"{time_colored}"
            f"{level_colored}"
            f"{file_line_colored}"
            f" {message_colored}"
            f"{self.COLORS['RESET']}"
        )
        
        return formatted_message

# Set up logging to use the colored formatter and include file info
def pytest_configure(config):
    """Configure pytest logging with custom formatter and handlers."""
    logger = logging.getLogger()
    handler = logging.StreamHandler(sys.stdout)
    
    # Apply custom formatting with file/line colorization
    formatter = ColoredFormatter('%(asctime)s', datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    
    # Add the handler to the logger and set the default log level
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)  # Default level for all logs
