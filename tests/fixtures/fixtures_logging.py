from __future__ import annotations

import logging
import os
import sys

from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
class LogFormatter(logging.Formatter):
    """
    Custom logging formatter that supports optional colorization.

    This formatter is intended to be used with logging handlers
    (e.g., StreamHandler for console output or FileHandler for file output).

    Formats log records with timestamps, log levels, filename and line numbers,
    and the log message itself. When `color=True`, it adds ANSI color codes for
    enhanced readability in terminals that support colors.

    Note:
        - The logging framework calls the `format()` method internally for each
          log record processed by the handler.
        - This class should be instantiated and passed to a handler's
          `setFormatter()`.
    """
    
    # Color palette for logs
    colors = {
        'DEBUG': '\033[94m',   # Blue
        'INFO': '\033[92m',    # Green
        'WARNING': '\033[93m', # Yellow
        'ERROR': '\033[91m',   # Red
        'CRITICAL': '\033[1;91m', # Bold Red
        'TIMESTAMP': '\033[90m', # Gray (for filename and line number)
        'MESSAGE': '\033[95m', # Purple
        'RESET': '\033[0m',
    }

    def __init__(self, color=False):
        super().__init__(fmt="%(asctime)s", datefmt="%Y-%m-%d %H:%M:%S")
        self.color = color

    def format(self, log):
        """Format the log record with colors and structured output."""
        super().format(log)
    
        level_color = (
            self.colors.get(log.levelname, self.colors['RESET'])
            if self.color else ''
        )
        time_color = self.colors['TIMESTAMP'] if self.color else ''
        file_color = self.colors['RESET'] if self.color else ''
        reset = self.colors['RESET'] if self.color else ''

        time_string = f"{time_color}[{log.asctime}]"
        level_string = f"{level_color}[{log.levelname}]"
        file_line_string = f"{file_color}[{log.filename}:{log.lineno}]"
        message_string = f"{level_color}{log.getMessage()}"

        return (
            f"{time_string}"
            f"{level_string}"
            f"{file_line_string}"
            f" {message_string}"
            f"{reset}"
    )

class LogConfigurator:
    """
    Encapsulates all logging setup for pytest runs.

    Responsibilities:
      - Creates console and file handlers.
      - Attaches appropriate formatters (with or without color).
      - Manages the root logger configuration.

    Important:
      - Depends on handlers to output logs.
      - Instantiates LogFormatter and assigns it to handlers.
      - Users of this class should call `configure()` to apply logging setup.
      - Handlers are specifically designed to work with LogFormatter.

    Usage example:
        config = LogConfigurator(log_dir="logs", level=logging.DEBUG)
        config.configure()

    """

    def __init__(self, log_dir="logs", level=logging.INFO):
        self.log_dir = log_dir
        self.level = level
        self.logger = logging.getLogger()

    def _create_console_handler(self):
        """
        Create a StreamHandler for console output.

        Applies color for use in terminals that support ANSI colors.

        Returns:
            logging.StreamHandler: Configured console handler.
        """
        handler = logging.StreamHandler(sys.stdout)
        formatter = LogFormatter(color=True)
        handler.setFormatter(formatter)
        return handler

    def _create_file_handler(self, timestamped=False):
        """
        Create a FileHandler to write logs to a file.

        Uses LogFormatter without color to keep log files clean and readable.

        Returns:
            logging.FileHandler: Configured file handler.
        """
        os.makedirs(self.log_dir, exist_ok=True)
        
        # If we want to keep old logs, we will save a second copy 
        # of the log with a timestamp in its filename
        if timestamped:
            log_filename = os.path.join(
                self.log_dir,
                f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
            )
        else:
            log_filename = os.path.join(self.log_dir, "latest.log")
        
        handler = logging.FileHandler(log_filename)
        formatter = LogFormatter(color=False)
        handler.setFormatter(formatter)
        return handler

    def configure(self):
        self.logger.handlers.clear()
        self.logger.setLevel(self.level)
        self.logger.addHandler(self._create_console_handler())
        self.logger.addHandler(self._create_file_handler())
        # If we want to keep old logs, we will save a second copy 
        # of the log with a timestamp in its filename
        if os.getenv("KEEP_OLD_LOGS", "false").lower() == "true":
            self.logger.addHandler(self._create_file_handler(timestamped=True))
