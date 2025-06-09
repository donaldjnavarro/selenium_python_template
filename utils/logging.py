
from __future__ import annotations

import logging
import os
import sys

# Define common constants
LOG_FORMAT = (
    "[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d] %(message)s"
)
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

LOG_COLORS = {
    'DEBUG': '\033[94m',   # Blue
    'INFO': '\033[92m',    # Green
    'WARNING': '\033[93m', # Yellow
    'ERROR': '\033[91m',   # Red
    'CRITICAL': '\033[1;91m', # Bold Red
    'TIMESTAMP': '\033[90m', # Gray (for filename and line number)
    'MESSAGE': '\033[95m', # Purple
    'RESET': '\033[0m',
}
def colorize_level(level_name: str) -> str:
    """Return the log level name wrapped in its ANSI color code."""
    color = LOG_COLORS.get(level_name.upper(), '')
    reset = LOG_COLORS['RESET']
    return f"{color}{level_name}{reset}" if color else level_name

def pre_logger():
    """Minimal logger setup for early-stage logging (before full config)."""
    prelogger_level = logging.INFO
    logging.basicConfig(
        level=prelogger_level,
        stream=sys.stdout,
        format=LOG_FORMAT,
        datefmt=DATE_FORMAT
    )
    logging.info(
        "Loading pre logger at level [{}]".format(
            colorize_level(logging.getLevelName(prelogger_level))
        )
    )

def main_logger():
    """Full logging configuration."""
    # DETERMINE LOG LEVEL TO ACTIVATE
    raw_level = os.getenv("LOG_LEVEL", "")
    LOG_LEVEL_NAME = raw_level.upper()
    VALID_LOG_LEVELS = set(logging._nameToLevel)
    if LOG_LEVEL_NAME not in VALID_LOG_LEVELS:
        raise ValueError(f"Invalid LOG_LEVEL in .env: '{raw_level}'")
    LOG_LEVEL = logging._nameToLevel[LOG_LEVEL_NAME]

    # Create logger
    logging.info(
        "Loading main logger at level [{}]".format(
            colorize_level(logging.getLevelName(LOG_LEVEL))
        )
    )
    LogConfigurator(level=LOG_LEVEL).configure()

class LogFormatter(logging.Formatter):
    """Custom logging formatter that supports optional colorization.

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

    # colors defined in file constants above
    colors = LOG_COLORS

    def __init__(self, color=False):
        super().__init__(fmt="%(asctime)s", datefmt=DATE_FORMAT)
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
            f"{level_string}"
            f"{time_string}"
            f"{file_line_string}"
            f" {message_string}"
            f"{reset}"
    )

class LogConfigurator:
    """Encapsulates all logging setup for pytest runs.

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
        config = LogConfigurator(level=logging.DEBUG)
        config.configure()

    """

    def __init__(self, level=logging.DEBUG):
        self.level = level
        self.logger = logging.getLogger()

    def _create_console_handler(self):
        """Create a StreamHandler for console output.

        Applies color for use in terminals that support ANSI colors.

        Returns:
            logging.StreamHandler: Configured console handler.

        """
        handler = logging.StreamHandler(sys.stdout)
        formatter = LogFormatter(color=True)
        handler.setFormatter(formatter)
        return handler

    def _create_file_handler(self, timestamped=False):
        """Create a FileHandler to write logs to a file.

        Uses LogFormatter without color to keep log files clean and readable.

        Returns:
            logging.FileHandler: Configured file handler.

        """        
        # If we want to keep old logs, we will save a second copy 
        # of the log with a timestamp in its filename
        if timestamped:
            log_filename = os.path.join(
                os.environ["TIMESTAMPED_REPORT_DIR"],
                "logs.log"
            )
        else:
            log_filename = os.path.join(
                os.environ["LATEST_REPORT_DIR"],
                "logs.log"
            )
        
        handler = logging.FileHandler(log_filename)
        formatter = LogFormatter(color=False)
        handler.setFormatter(formatter)
        return handler

    def configure(self):
        """Configure the main logger with all enhancements"""
        self.logger.handlers.clear()
        self.logger.setLevel(self.level)
        self.logger.addHandler(self._create_console_handler())
        self.logger.addHandler(self._create_file_handler())
        # If we want to keep old logs, we will save a second copy 
        # of the log with a timestamp in its filename
        if os.getenv("SAVE_HISTORICAL_REPORTS", "false").lower() == "true":
            self.logger.addHandler(self._create_file_handler(timestamped=True))
