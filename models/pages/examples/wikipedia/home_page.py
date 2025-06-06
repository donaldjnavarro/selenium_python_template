from __future__ import annotations
from selenium.webdriver.common.by import By
from models.pages.base_page import BasePage
from utils.timing import Timing
from utils.dom import save_dom_on_failure

class WikipediaHomePage(BasePage):
    """Page object model for the Wikipedia home page"""

    URL = "https://www.wikipedia.org"
    TITLE = "Wikipedia"
    LOCATORS = {
        "search_box": (By.XPATH, "//input[@name='search']")
    }

    @save_dom_on_failure(
        lambda self: f"{self.__class__.__name__}_is_loaded_failed.html"
    )
    def is_loaded(self):
        """Check required elements have loaded"""
        super().is_loaded() # Inherit checks from BasePage
        
        Timing.wait_until_true(
            lambda: self.get_element("search_box").is_displayed(),
            message="Search box is not displayed on the Wikipedia home page."
        )

    def search(self, query: str):
        """Type into the search box and submit it"""
        search_box = self.get_element("search_box")
        search_box.send_keys(query)
        search_box.submit()
