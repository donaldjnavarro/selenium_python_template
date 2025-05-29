
"""Pytest shared fixtures"""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import logging
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService

# Webdriver Manager configuration to control where the driver cache ends up
import os
os.environ["WDM_LOCAL"] = "1"
os.environ["WDM_CACHE_DIR"] = os.path.abspath("drivers_cache")

# Load .env file
from dotenv import load_dotenv
load_dotenv()

# Determine if the .env file has been configured to force the tests to run in headless mode
headless = os.getenv("HEADLESS", "false").lower() == "true"

# Browser fixtures
@pytest.fixture(params=["chrome", "firefox", "edge"])
def driver(request):
    """Cross browser handling for webdriver calls"""
    browser = request.param

    # Chrome
    if browser == "chrome":
        # Chrome base options
        options = ChromeOptions()

        # Headless Chrome configuration
        if headless:
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

        # Create the Chrome driver instance
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    # Firefox
    elif browser == "firefox":
        # Firefox base options
        options = FirefoxOptions()

        # Headless Firefox configuration
        if headless:
            # options.headless = True # The official way to set headless mode in Firefox
            options.add_argument("--headless=new") # Force the newest headless mode approach, especially for CICD
            options.add_argument("--width=1920")
            options.add_argument("--height=1080")

        # Create the Firefox driver instance
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)

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
        driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)

    else:
        raise ValueError(f"Unsupported browser: {browser}")

    driver.maximize_window()
    yield driver
    driver.quit()

def pytest_addoption(parser):
    """Space for adding custom command line options for pytest"""
    pass

def pytest_configure(config):
    """Print statements will only display in the commandline if the .env file is configured to allow it"""
    # Load env variable, default to false
    print_output = os.getenv("DISPLAY_PRINTS", "false").lower() == "true"

    if print_output:
        # Disable output capture (equivalent to -s when running pytest)
        config.option.capture = "no"

@pytest.fixture(autouse=True, scope="session")
def configure_logging():
    log_cli = os.getenv("LOG_CLI", "false").lower() == "true"
    if not log_cli:
        return

    # Set the level of log that will print. Everything more severe than this will be printed. Also define a default if the .env variable is not set
    log_level_str = os.getenv("LOG_LEVEL", "WARNING").upper()
    log_level = getattr(logging, log_level_str, logging.DEBUG)

    # Silence all trivial logs from external libraries
    logging.getLogger().setLevel(logging.WARNING)

    # Configure root logger for pytest to capture
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

    # Optional: if you want to control specific library logs, do here
    # logging.getLogger("selenium").setLevel(logging.WARNING)

def pytest_collection_modifyitems(config, items):
    """pytest hook to skip tests based on user configurations"""
    skip = pytest.mark.skip(reason="Skipping tests that require secrets")
    for item in items:
        if "secrets" in item.keywords:
            if os.getenv("SKIP_SECRETS", "true").lower() == "true":
                item.add_marker(skip)
