from __future__ import annotations

from selenium.webdriver.remote.webdriver import WebDriver

from utils.timing import Timing

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
    
    def is_loaded(self):
        """Wait until page is finished loading by checking required elements
        
        This can be overridden or expanded in individual page models.
        """       
        if self.URL is not None:
            Timing.wait_until_true(lambda: self.URL in self.driver.current_url)
        
        if self.TITLE is not None:
            Timing.wait_until_true(lambda: self.TITLE in self.driver.title)

        return True

    def load(self):
        """Load the page in the browser.

        Raises:
            NotImplementedError: If the URL is not defined in the subclass.

        """
        if not self.URL:
            raise NotImplementedError("Subclasses must define a URL.")
        self.driver.get(self.URL)
        self.is_loaded()
