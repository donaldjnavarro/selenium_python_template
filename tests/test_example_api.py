import json
import requests
import os
import logging
import pytest
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

def test_example_postman_echo_get():
    """Example test for a GET request using Postman Echo API"""

    # Establish test parameters
    url = "https://postman-echo.com/get"
    params = {"foo1": "bar1", "foo2": "bar2"}

    # Send the GET request
    response = requests.get(url, params=params)

    # Confirm the request was accepted
    assert response.status_code == 200, "Expected API request {} with params {} to return status code 200, but received: {}".format(url, params, response.status_code)
    
    # Confirm the contents of the response
    data = response.json()
    assert data["args"] == params, "Expected API request {} to echo back the attached parameters {}, but received: {}".format(url, params, data["args"])

def test_example_postman_echo_post():
    """Example test for a POST request using Postman Echo API"""

    # Establish test parameters
    url = "https://postman-echo.com/post"
    payload = {"key": "value"}

    # Send the POST request
    response = requests.post(url, json=payload)

    # Confirm the request was accepted
    assert response.status_code == 200, "Expected API request {} with payload {} to return status code 200, but received: {}".format(url, payload, response.status_code)

    # Confirm the contents of the response
    data = response.json()
    assert data["json"] == payload, "Expected API request {} to echo back the attached payload {}, but received: {}".format(url, payload, data["json"])


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
    response = requests.get(url, auth=(requests.auth.HTTPBasicAuth(postman_username, postman_password)))

    # Confirm the request was accepted
    assert response.status_code == 200, "Expected API request {} to return status code 200, but received: {}".format(url, response.status_code)

    # Confirm the contents of the response
    responseJson = json.loads(response.text)
    assert responseJson == { "authenticated": True }, "Expected API request {} to respond with JSON authenticated: true but received: {}".format(url, responseJson)

if __name__ == '__main__':
    test_example_postman_echo_get()
    test_example_postman_echo_post()
    test_example_postman_basic_auth()
