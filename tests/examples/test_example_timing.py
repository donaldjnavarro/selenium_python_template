"""Examples of timing utilities being used in Selenium tests.

NOTE: These examples include both successful waits
and those that are expected to timeout

The negative case examples will pass within pytest 
but they will still display their error messages 
to illustrate what exceptions will look like
"""
# Standard library imports
from __future__ import annotations
import pytest
from selenium.webdriver.common.by import By
from utils.timing import Timing
from models.pages.examples.wikipedia.home_page import WikipediaHomePage

OVERRIDE_DEFAULT_TIMEOUT_FOR_DEMO = 2

@pytest.mark.visible
@pytest.mark.example
def test_wait_until_visible_success(driver):
    home_page = WikipediaHomePage(driver)
    home_page.load()
    
    # Wait for an obvious element
    element = Timing.wait_until_visible(
        driver,
        By.XPATH,
        "//main//img",
        timeout=OVERRIDE_DEFAULT_TIMEOUT_FOR_DEMO,
        )
    assert element.is_displayed()

@pytest.mark.visible
@pytest.mark.example
@pytest.mark.error
def test_wait_until_visible_timeout(driver):

    home_page = WikipediaHomePage(driver)
    home_page.load()

    # Permit test to pass as long as the exception raised is expected
    with pytest.raises(TimeoutError):
        # Should raise: No element with this ID
        Timing.wait_until_visible(
            driver,
            By.ID,
            "nonexistent-element",
            timeout=OVERRIDE_DEFAULT_TIMEOUT_FOR_DEMO,
        )

@pytest.mark.clickable
@pytest.mark.example
def test_wait_until_clickable_success(driver):
    home_page = WikipediaHomePage(driver)
    home_page.load()
    
    # Wait until an obvious button is clickable
    element = Timing.wait_until_clickable(
        driver,
        By.XPATH,
        "//button[@type = 'submit']",
        timeout=OVERRIDE_DEFAULT_TIMEOUT_FOR_DEMO,
    )
    assert element.is_enabled()

@pytest.mark.clickable
@pytest.mark.example
@pytest.mark.error
def test_wait_until_clickable_timeout(driver):
    home_page = WikipediaHomePage(driver)
    home_page.load()

    # Permit test to pass as long as the exception raised is expected
    with pytest.raises(TimeoutError):
        # Wait for an element that will never be clickable
        # (Since it doesn't exist)
        Timing.wait_until_clickable(
            driver,
            By.ID,
            "not-real-element",
            timeout=OVERRIDE_DEFAULT_TIMEOUT_FOR_DEMO,
        )

@pytest.mark.invisible
@pytest.mark.example
def test_wait_until_invisible_success(driver):
    home_page = WikipediaHomePage(driver)
    home_page.load()

    # Verify that waiting for an element to be not-visible works
    # (Since the element is not on the page)
    assert Timing.wait_until_invisible(
        driver,
        By.ID,
        "not-on-page",
        timeout=OVERRIDE_DEFAULT_TIMEOUT_FOR_DEMO,
    )
    elements = driver.find_elements(By.ID, "not-on-page")
    assert len(elements) == 0

@pytest.mark.invisible
@pytest.mark.example
@pytest.mark.error
def test_wait_until_invisible_timeout(driver):
    home_page = WikipediaHomePage(driver)
    home_page.load()

    # Permit test to pass as long as the exception raised is expected
    with pytest.raises(TimeoutError):
        # Verify that timeout errors when waiting for 
        # an element to become invisible that never does
        Timing.wait_until_invisible(
            driver,
            By.XPATH,
            "//main//img",
            timeout=OVERRIDE_DEFAULT_TIMEOUT_FOR_DEMO,
        )

@pytest.mark.wait_true
@pytest.mark.example
def test_wait_until_true_success(driver):
    home_page = WikipediaHomePage(driver)
    home_page.load()

    # Verify waiting for an obvios condition to be true
    Timing.wait_until_true(lambda: 2 + 2 == 4)

@pytest.mark.wait_true
@pytest.mark.example
@pytest.mark.error
def test_wait_until_true_timeout(driver):
    home_page = WikipediaHomePage(driver)
    home_page.load()

    # Permit test to pass as long as the exception raised is expected
    with pytest.raises(TimeoutError):
        # Verify that timeout errors when waiting for
        # a condition that never becomes true
        Timing.wait_until_true(
            lambda: False,
            timeout=OVERRIDE_DEFAULT_TIMEOUT_FOR_DEMO,
            message="Demonstrating a timeout error in wait_until_true"
        )

@pytest.mark.wait_true
@pytest.mark.example
@pytest.mark.error
def test_wait_until_true_on_timeout_hook(driver):
    home_page = WikipediaHomePage(driver)
    home_page.load()

    # Define the action to be called on timeout
    timeout_action = {"called": False}
    def on_timeout_action():
        # A simple proof that the action was called
        timeout_action["called"] = True

    # Permit test to pass as long as the exception raised is expected
    with pytest.raises(TimeoutError):
        # Verify that on_timeout hook is called when condition is never true
        Timing.wait_until_true(
            lambda: False,
            timeout=OVERRIDE_DEFAULT_TIMEOUT_FOR_DEMO,
            on_timeout=on_timeout_action
        )
    assert timeout_action["called"], (
        "on_timeout action was not called after timeout error"
    )
