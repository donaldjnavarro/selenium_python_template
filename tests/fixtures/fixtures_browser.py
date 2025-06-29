"""Fixtures for handling browsers"""

# Standard imports
from __future__ import annotations
import os

__all__ = ['driver']  # Public fixture

# Local imports
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# Launch the logger
import logging
logger = logging.getLogger()

# Browser fixtures
browserConfigs = {
    "chrome": os.getenv("CHROME", "true").lower() == "true",
    "firefox": os.getenv("FIREFOX", "true").lower() == "true",
    "edge": os.getenv("EDGE", "true").lower() == "true"
}

DEFAULT_BROWSER_WIDTH = os.environ.get("BROWSER_WIDTH", "1920")
DEFAULT_BROWSER_HEIGHT = os.environ.get("BROWSER_HEIGHT", "1080")
def apply_window_size(
    driver,
    headless: bool,
    width=DEFAULT_BROWSER_WIDTH,
    height=DEFAULT_BROWSER_HEIGHT
):
    """Resize the window"""
    driver.set_window_size(int(width), int(height))

browserCoverage = [name for name, enabled in browserConfigs.items() if enabled]
@pytest.fixture(params=browserCoverage)
def driver(request):
    """Cross browser handling for webdriver calls"""
    logger.info("Running driver() in fixtures_browser.py")
    browser = request.param

    # Determine if the .env file has been configured for headless mode
    headless = os.environ.get("HEADLESS", "false").lower() == "true"

    # Chrome
    if browser == "chrome":
        # Chrome base options
        options = ChromeOptions()

        # Headless Chrome configuration
        if headless:
            options.add_argument("--disable-gpu")
            options.add_argument(f"--window-size={DEFAULT_BROWSER_WIDTH},{DEFAULT_BROWSER_HEIGHT}")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--log-level=3")  # Suppress INFO/WARNING logs

            # Use new headless mode if Chrome version supports it
            options.add_argument("--headless=new")


        # Create the Chrome driver instance
        chrome_path = ChromeDriverManager().install()
        driver = webdriver.Chrome(
            service=ChromeService(chrome_path),
            options=options
        )
        logger.info(
            f"Chrome version: "
            f"{driver.capabilities['chrome']['chromedriverVersion']}"
        )

    # Firefox
    elif browser == "firefox":
        # Firefox base options
        options = FirefoxOptions()

        # Headless Firefox configuration
        if headless:
            # # The official way to set headless mode in Firefox
            # options.headless = True
            # Force the newest headless mode approach, especially for CICD
            options.add_argument("--headless=new")
            options.add_argument(f"--width={DEFAULT_BROWSER_WIDTH}")
            options.add_argument(f"--height={DEFAULT_BROWSER_HEIGHT}")

        # Create the Firefox driver instance
        gecko = GeckoDriverManager().install()
        driver = webdriver.Firefox(
            service=FirefoxService(gecko),
            options=options
        )
        logger.info(
            f"Firefox version: {driver.capabilities['browserVersion']}"
        )

    # Edge
    elif browser == "edge":
        # Edge base options
        options = EdgeOptions()

        # Headless Edge configuration
        if headless:
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument(f"--window-size={DEFAULT_BROWSER_WIDTH},{DEFAULT_BROWSER_HEIGHT}")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
        
        # Create the Edge driver instance
        edge_path = EdgeChromiumDriverManager().install()
        driver = webdriver.Edge(
            service=EdgeService(edge_path),
            options=options
        )
        logger.info(f"Edge version: {driver.capabilities['browserVersion']}")

    else:
        raise ValueError(f"Unsupported browser: {browser}")

    apply_window_size(driver, headless)
    yield driver
    driver.quit()
