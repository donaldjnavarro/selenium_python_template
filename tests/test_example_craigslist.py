"""Example snippets for Python automated testing using Craigslist as a test subject"""
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys

def test_example_craigslist(driver):
    """Example Selenium testL Craigslist"""

    # Navigate to Craigslist
    driver.get("https://newyork.craigslist.org")

    # Confirm the page loaded correctly
    landing_title = "craigslist: new york jobs"
    assert landing_title in driver.title, "Expected '{}' to be in the page title, but received: '{}'".format(landing_title, driver.title)

    # Take an action on the page
    input_text = "car"
    search_box = driver.find_element(By.XPATH, "//*[@id = 'leftbar']//input[@placeholder = 'search craigslist']")
    search_box.send_keys(input_text)
    search_box.send_keys(Keys.ENTER)
    time.sleep(3)

    # Confirm the results of the action
    search_results_title = "new york for sale \"{}\"".format(input_text)
    assert search_results_title in driver.title, "Expected '{}' to be in the page title, but received: '{}'".format(search_results_title, driver.title)

    # Clean up
    driver.quit()

if __name__ == "__main__":
        test_example_craigslist()
