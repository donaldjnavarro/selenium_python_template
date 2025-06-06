from __future__ import annotations

from selenium.webdriver.remote.webdriver import WebDriver

from utils.timing import Timing
from utils.dom import save_dom_on_failure

class BasePage:
    """Base class for all page objects.

    Specific pages that inherit this POM should override the URL.
    """

    # URL needs to be defined in page models that inherit this class
    URL = None

    # TITLE needs to be defined in page models that inherit this class
    TITLE = None

    # LOCATORS need to be defined as tuples of (By, value) 
    # by page models that inherit this class
    LOCATORS = {}

    def __init__(self, driver: WebDriver):
        self.driver = driver
    
    def get_element(self, name: str):
        """Get an element using Selenium
        
        Args:
            name (str): The key for the locator in the LOCATORS dict.

        Returns:
            WebElement: The found web element.

        Raises:
            ValueError: If the locator is not found in LOCATORS.

        """
        locator = self.LOCATORS.get(name)
        if locator is None:
            raise ValueError(f"Locator '{name}' not found in LOCATORS.")
        return self.driver.find_element(*locator)
    
    @save_dom_on_failure(
        lambda self: f"{self.__class__.__name__}_is_loaded_failed.html"
    )
    def is_loaded(self, timeout: float = 10.0):
        """Wait until the page is finished loading by checking URL and title.

        Raises AssertionError with debug artifacts if the condition fails.
        """
        if self.URL is not None:
            Timing.wait_until_true(
                lambda: self.URL in self.driver.current_url,
                timeout=timeout,
                message=(
                    f"Expected URL to contain '{self.URL}' "
                    f"but got '{self.driver.current_url}'"
                )
            )

        if self.TITLE is not None:
            Timing.wait_until_true(
                lambda: self.TITLE in self.driver.title,
                timeout=timeout,
                message=(
                    f"Expected title to contain '{self.TITLE}' "
                    f"but got '{self.driver.title}'"
                )
            )

        return True

    def load(self):
        """Load the page in the browser.

        Raises:
            NotImplementedError: If the URL is not defined in the subclass.

        """
        if not self.URL:
            raise NotImplementedError("Page model failed to define a URL.")
        self.driver.get(self.URL)
        self.is_loaded()
