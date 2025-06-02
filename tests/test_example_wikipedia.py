"""
Example snippets for Python automated testing using Wikipedia as a test subject
"""
# Standard library imports
from __future__ import annotations

# Third-party imports
import pytest

# Local imports
from utils.timing import Timing
from pages.examples.wikipedia.home_page import WikipediaHomePage
from pages.examples.wikipedia.search_results_page import (
    WikipediaSearchResultsPage,
)

@pytest.mark.example
def test_example_wikipedia(driver):
    """Example Selenium test: Wikipedia"""

    home_page = WikipediaHomePage(driver)
    # Navigate to Wikipedia
    home_page.load()
    
    # Confirm Wikipedia home page loaded
    assert home_page.TITLE in driver.title, (
        f"Expected Wikipedia landing page title to contain: "
        f"'{home_page.TITLE}'"
        f"But actual: '{driver.title}'"
    )

    # Take an action on the page
    input_text = "Selenium UI automation"
    home_page.search(input_text)

    # Verify the results of the action
    search_results_page = WikipediaSearchResultsPage(driver)
    search_results_page.is_loaded()

    # Confirm Wikipedia search results page loaded for the search input
    expected_search_results_title = f"{input_text}"
    f"{expected_search_results_title.TITLE}"

    Timing.wait_until_true(
        lambda: expected_search_results_title in
        driver.title
    )
    assert expected_search_results_title in driver.title, (
        f"Expected Wikipedia search results page title to contain: "
        f"'{expected_search_results_title}' "
        f"but actual: '{driver.title}'"
    )

    # Clean up
    driver.quit()

if __name__ == "__main__":
        test_example_wikipedia()
