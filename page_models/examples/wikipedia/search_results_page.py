from __future__ import annotations
from pages.base_page import BasePage

class WikipediaSearchResultsPage(BasePage):
    """Page object model for the Wikipedia search results page"""

    # Partial URL depends on search details
    URL = "https://en.wikipedia.org/wiki"
    # Partial page title: Full text will be 
    # `lorem ipsum - Search results - Wikipedia`
    # based on the search terms
    TITLE = "- Search results - Wikipedia"
    LOCATORS = {}
