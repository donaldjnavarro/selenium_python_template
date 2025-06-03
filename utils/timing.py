
# Standard imports
from __future__ import annotations

# Third-party imports
import logging
import os
import time

# Local imports
from dotenv import load_dotenv
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Environmental variables
load_dotenv()

# Logging tools
logger = logging.getLogger(__name__)


class Timing:
    """Utility class for handling timing actions"""

    @staticmethod
    def wait_until_visible(driver, by, value, timeout=10):
        """Wait for element to be visible"""
        return WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((by, value))
        )

    @staticmethod
    def wait_until_clickable(driver, by, value, timeout=10):
        """Wait for element to be clickable"""
        return WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )

    @staticmethod
    def wait_until_invisible(driver, by, value, timeout=10):
        """Wait for element to be invisible"""
        return WebDriverWait(driver, timeout).until(
            EC.invisibility_of_element_located((by, value))
        )
    
    @staticmethod
    def wait_until_true(condition, timeout=None, interval=0.5, message=None):
        """Wait for a callback to return True within the given timeout

        Fails with AssertionError if the condition is not met in time.
        :param condition: When this is true, the wait stops.
        :param timeout: Max wait time (overrides .env value if provided).
        :param interval: Polling interval in seconds.
        :param message: Optional message to show if assertion fails.
        """
        max_wait = timeout or int(os.getenv("DEFAULT_WAIT_TIMEOUT", 10))
        end_time = time.time() + max_wait
        last_error = None

        while time.time() < end_time:
            try:
                if condition():
                    return
            except Exception as e:
                last_error = e
            time.sleep(interval)

        if last_error:
            logger.error(
                f"Error after {max_wait} seconds: {last_error}"
            )
        logger.error(
            f"Condition failed after {max_wait} seconds."
            "If the subsequent assertion did not fail, this may indicate "
            "test maintenance is needed to avoid an unnecessary wait."
            # Message will be included if it was provided to this function
            f"\n{message}" if message else ""
        )
