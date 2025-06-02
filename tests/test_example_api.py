# tests/test_postman_echo.py
import os
import pytest
from dotenv import load_dotenv
from models.apis.examples.postman_api import PostmanEchoAPI

load_dotenv()

@pytest.mark.example
def test_example_postman_echo_get():
    """Example API request: GET with query parameters"""
    api = PostmanEchoAPI()
    params = {"foo1": "bar1", "foo2": "bar2"}

    response = api.echo_get(params)
    assert response.status_code == 200
    assert response.json()["args"] == params

@pytest.mark.example
def test_example_postman_echo_post():
    """Example API request: POST with JSON"""
    api = PostmanEchoAPI()
    payload = {"key": "value"}

    response = api.echo_post(payload)
    assert response.status_code == 200
    assert response.json()["json"] == payload

@pytest.mark.example
@pytest.mark.secrets
def test_example_postman_basic_auth():
    """Example API request using Basic Authentication"""

    username = os.getenv("POSTMAN_USERNAME")
    password = os.getenv("POSTMAN_PASSWORD")
    assert username and password, (
        "Missing POSTMAN_USERNAME or POSTMAN_PASSWORD in .env"
    )

    api = PostmanEchoAPI().with_auth(username, password)
    response = api.basic_auth()

    assert response.status_code == 200
    assert response.json() == {"authenticated": True}
