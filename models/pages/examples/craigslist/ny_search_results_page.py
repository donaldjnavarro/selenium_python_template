from __future__ import annotations
from models.pages.base_page import BasePage

class NYCraigslistSearchResultsPage(BasePage):
    """Page object model for the NY Craigslist search results page"""

    # Partial URL depends on search details
    URL = "https://newyork.craigslist.org/search/"
    # Partial page title: Full text will be 
    # `new york for sale "lorem ipsum"`
    # based on the search terms
    TITLE = "new york for sale"
    LOCATORS = {}
