"""
Example snippets for Python automated testing using Wikipedia as a test subject
"""
# Standard library imports
from __future__ import annotations

# Third-party imports
import pytest

# Local imports
from models.pages.examples.wikipedia.home_page import WikipediaHomePage
from models.pages.examples.wikipedia.search_results_page import (
    WikipediaSearchResultsPage,
)

@pytest.mark.example
@pytest.mark.wikipedia
def test_example_wikipedia(driver):
    """Example Selenium test: Wikipedia"""

    # Navigate to Wikipedia
    home_page = WikipediaHomePage(driver)
    home_page.load()
    
    # Confirm Wikipedia home page loaded
    assert home_page.TITLE in driver.title, (
        f"Expected Wikipedia landing page title to contain: "
        f"'{home_page.TITLE}'"
        f"But actual: '{driver.title}'"
    )

    # Take an action: Search Wikipedia
    input_text = "Selenium UI automation"
    home_page.search(input_text)

    # Verify the search results page loaded
    search_results_page = WikipediaSearchResultsPage(driver)
    search_results_page.is_loaded()

    # Verify the page title includes search terms
    expected_search_results_title = f"{input_text}"
    f"{search_results_page.TITLE}"
    assert expected_search_results_title in driver.title, (
        f"Expected Wikipedia search results page title to contain: "
        f"'{expected_search_results_title}' "
        f"but actual: '{driver.title}'"
    )

    # Clean up
    driver.quit()

if __name__ == "__main__":
    test_example_wikipedia()
