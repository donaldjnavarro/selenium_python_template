
# Standard imports
from __future__ import annotations

# Third-party imports
import os
import time

# Local imports
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Logging tools
import logging
logger = logging.getLogger()

# Default timeout
DEFAULT_TIMEOUT = int(os.getenv("MAX_WAIT", 10))

class Timing:
    """Utility class for handling timing actions"""

    @staticmethod
    def wait_until_visible(driver, by, value, timeout=DEFAULT_TIMEOUT):
        """Wait for element to be visible"""
        try:
            return WebDriverWait(driver, timeout).until(
                EC.visibility_of_element_located((by, value))
            )
        except Exception as e:
            message = (
                f"Element located by ({by}, {value}) was "
                f"not visible after {timeout} seconds: {e}"
            )
            logger.error(message)
            raise TimeoutError(message) from e

    @staticmethod
    def wait_until_clickable(driver, by, value, timeout=DEFAULT_TIMEOUT):
        """Wait for element to be clickable"""
        try:
            return WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
        except Exception as e:
            message = (
                f"Element located by ({by}, {value}) was "
                f"not clickable after {timeout} seconds: {e}"
            )
            logger.error(message)
            raise TimeoutError(message) from e

    @staticmethod
    def wait_until_invisible(driver, by, value, timeout=DEFAULT_TIMEOUT):
        """Wait for element to be invisible"""
        try:
            return WebDriverWait(driver, timeout).until(
                EC.invisibility_of_element_located((by, value))
            )
        except Exception as e:
            message = (
                f"Element located by ({by}, {value}) was "
                f"not invisible after {timeout} seconds: {e}"
            )
            logger.error(message)
            raise TimeoutError(message) from e
    
    @staticmethod
    def wait_until_true(
        condition,
        timeout=DEFAULT_TIMEOUT,
        interval=0.5,
        message=None,
        on_timeout=None
    ):
        """Wait for a custom condition to return True.

        Args:
            condition (callable): Your check function.
            timeout (float): Max time to wait in seconds.
            interval (float): Time between checks.
            message (str): Optional custom error message.
            on_timeout (callable): Optional hook to run before raising.

        """
        end_time = time.time() + timeout

        while time.time() < end_time:
            try:
                # Condition met!
                if condition():
                    return
            except Exception as e:
                logger.debug(f"Wait condition raised an exception: {e}")
            time.sleep(interval)

        if on_timeout:
            try:
                on_timeout()
            except Exception as e:
                logger.warning(f"on_timeout() raised: {e}")

        final_message = message or (
            f"Condition not met within {timeout} seconds."
        )
        logger.error(final_message)
        raise TimeoutError(final_message)
