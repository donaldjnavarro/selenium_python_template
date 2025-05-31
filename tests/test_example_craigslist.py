"""
Example tests for Craigslist website
"""
# Standard library imports
from __future__ import annotations

# Third-party imports
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Local imports
from utils.timing import Timing


@pytest.mark.example
def test_example_craigslist(driver):
    """Example Selenium testL Craigslist"""

    # Navigate to Craigslist
    driver.get("https://newyork.craigslist.org")

    # Confirm the page loaded correctly
    landing_title = "craigslist: new york jobs"
    assert landing_title in driver.title, (
        "Expected '{}' to be in the page title, but received: '{}'".format(
            landing_title, driver.title
        )
    )

    # Take an action on the page
    input_text = "car"
    search_box = driver.find_element(
        By.XPATH, (
            "//*[@id = 'leftbar']//input[@placeholder = 'search craigslist']"
        )
    )
    search_box.send_keys(input_text)
    search_box.send_keys(Keys.ENTER)

    # Confirm the results of the action
    search_results_title = "new york for sale \"{}\"".format(input_text)
    Timing.wait_until_true(lambda: search_results_title in driver.title)
    assert search_results_title in driver.title, (
        "Expected '{}' to be in the page title, but received: '{}'".format(
              search_results_title, driver.title
        )
    )

    # Clean up
    driver.quit()

if __name__ == "__main__":
        test_example_craigslist()
