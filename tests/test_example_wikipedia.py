"""
Example snippets for Python automated testing using Wikipedia as a test subject
"""
# Standard library imports
from __future__ import annotations

# Third-party imports
import pytest
from selenium.webdriver.common.by import By

# Local imports
from utils.timing import Timing


@pytest.mark.example
def test_example_wikipedia(driver):
    """Example Selenium test: Wikipedia"""

    # Navigate to Wikipedia
    driver.get("https://www.wikipedia.org")
    
    # Confirm the page loaded
    landing_title = "Wikipedia"
    assert landing_title in driver.title, (
        "Expected '{}' to be in the page title, but received: '{}'".format(
            landing_title, driver.title
        )
    )

    # Take an action on the page
    input_text = "Selenium UI automation"
    search_box = driver.find_element(By.NAME, "search")
    search_box.send_keys(input_text)
    search_box.submit()

    # Confirm the results of the action
    search_results_title = "{} - Search resultsXXX".format(input_text)
    Timing.wait_until_true(lambda: search_results_title in driver.title)
    assert search_results_title in driver.title, (
        "Expected '{}' to be in the page title, but received: '{}'".format(
            search_results_title, driver.title
        )
    )

    # Clean up
    driver.quit()

if __name__ == "__main__":
        test_example_wikipedia()
