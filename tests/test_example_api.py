"""
Example tests that use API requests
"""
# Standard library imports
from __future__ import annotations

# Third-party imports
import json
import logging
import os

# Local imports
import pytest
import requests
from dotenv import load_dotenv

import logging
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

# Environmental variables
load_dotenv()

# Logging tools
logger = logging.getLogger(__name__)

@pytest.mark.example
def test_example_postman_echo_get():
    """Example test for a GET request using Postman Echo API"""

    # Establish test parameters
    url = "https://postman-echo.com/get"
    params = {"foo1": "bar1", "foo2": "bar2"}

    # Send the GET request
    response = requests.get(url, params=params)

    # Confirm the request was accepted
    assert response.status_code == 200, (
        f"API request {url} with params {params}"
        f"Expected: Status code 200"
        f"Actual: {response.status_code}"
    )
    
    # Confirm the contents of the response
    data = response.json()
    assert data["args"] == params, (
        f"API request {url}"
        f"Expected: Response echo {params}"
        f"Actual: {data["args"]}"
    )

@pytest.mark.example
def test_example_postman_echo_post():
    """Example test for a POST request using Postman Echo API"""

    # Establish test parameters
    url = "https://postman-echo.com/post"
    payload = {"key": "value"}

    # Send the POST request
    response = requests.post(url, json=payload)

    # Confirm the request was accepted
    assert response.status_code == 200, (
        f"API request {url} with payload {payload}"
        f"Expected: Status code 200"
        f"Actual: {response.status_code}"
    )

    # Confirm the contents of the response
    data = response.json()
    assert data["json"] == payload, (
        f"API request {url}"
        f"Expected: Response payload {payload}"
        f"Actual: {data["json"]}"
    )

@pytest.mark.example
@pytest.mark.secrets
def test_example_postman_basic_auth():
    """Example test for API requests using Basic Authentication"""

    # Establish test parameters
    url = "https://postman-echo.com/basic-auth"
    postman_username = os.getenv("POSTMAN_USERNAME")
    postman_password = os.getenv("POSTMAN_PASSWORD")
    if (not postman_username or not postman_password):
        raise RuntimeError("Postman credentials not found in .env file")

    # Send the POST request
    # response = requests.get(url, auth=(postman_username, postman_password))
    response = requests.get(
        url,
        auth=(requests.auth.HTTPBasicAuth(postman_username, postman_password))
    )

    # Confirm the request was accepted
    assert response.status_code == 200, (
        f"API request {url}"
        f"Expected: Status code 200"
        f"Actual: {response.status_code}"
    )

    # Confirm the contents of the response
    responseJson = json.loads(response.text)
    assert responseJson == { "authenticated": True }, (
        f"Expected API request {url} to respond with JSON authenticated: true"
        f"but received: {responseJson}"
    )

if __name__ == '__main__':
    test_example_postman_echo_get()
    test_example_postman_echo_post()
    test_example_postman_basic_auth()
