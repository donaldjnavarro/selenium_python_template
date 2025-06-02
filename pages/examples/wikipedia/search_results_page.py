from __future__ import annotations
from pages.base_page import BasePage

class WikipediaSearchResultsPage(BasePage):
    """Page object model for the Wikipedia search results page"""

    URL = "https://en.wikipedia.org/wiki" # Partial URL depends on search details
    TITLE = "- Search results - Wikipedia"
    LOCATORS = {}
