"""
Example tests for Craigslist website
"""
# Standard library imports
from __future__ import annotations

# Third-party imports
import pytest

# Local imports
from page_models.examples.craigslist.ny_home_page import NYCraigslistHomePage
from page_models.examples.craigslist.ny_search_results_page import (
    NYCraigslistSearchResultsPage,
)


@pytest.mark.example
def test_example_craigslist(driver):
    """Example Selenium test of the Craigslist website"""

    # Navigate to Craigslist
    craigslist_home_page = NYCraigslistHomePage(driver)
    craigslist_home_page.load()

    # Confirm the Craigslist home page loaded
    assert craigslist_home_page.TITLE in driver.title, (
        f"Expected '{craigslist_home_page.TITLE}' to be in the page title, "
        f"but received: '{driver.title}'"
    )

    # Take an action: Search site
    input_text = "car"
    craigslist_home_page.search(input_text)

    # Confirm the search results page loaded
    search_results_page = NYCraigslistSearchResultsPage(driver)
    search_results_page.is_loaded()

    # Verify page title includes search terms
    search_results_title = f"{search_results_page.TITLE} \"{input_text}\""
    assert search_results_title in driver.title, (
        f"Expected '{search_results_title}' to be in the page title, "
        f"but received: '{driver.title}'"
    )

    # Clean up
    driver.quit()

if __name__ == "__main__":
        test_example_craigslist()
