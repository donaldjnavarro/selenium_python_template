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
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

            # Use new headless mode if Chrome version supports it
            options.add_argument("--headless=new")


        # Create the Chrome driver instance
        driver = webdriver.Chrome(
            service=ChromeService(
                ChromeDriverManager().install()
            ), options=options
        )

        version = driver.capabilities['chrome']['chromedriverVersion']
        logger.info(f"Chrome version: {version}")

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
            options.add_argument("--width=1920")
            options.add_argument("--height=1080")

        # Create the Firefox driver instance
        gecko = GeckoDriverManager().install()
        service = FirefoxService(gecko)
        driver = webdriver.Firefox(service=service, options=options)
        firefox_version = driver.capabilities['browserVersion']
        logger.info(f"Firefox version: {firefox_version}")

    # Edge
    elif browser == "edge":
        # Edge base options
        options = EdgeOptions()

        # Headless Edge configuration
        if headless:
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
        
        # Create the Edge driver instance
        driver = webdriver.Edge(
            service=EdgeService(
                EdgeChromiumDriverManager().install()
            ), options=options
        )
        edge_version = driver.capabilities['browserVersion']
        logger.info(f"Edge version: {edge_version}")
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    driver.maximize_window()
    yield driver
    driver.quit()
