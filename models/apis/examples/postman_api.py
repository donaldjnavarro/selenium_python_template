# api_models/postman_echo.py
from models.apis.base_api import BaseAPI

class PostmanEchoAPI(BaseAPI):
    """API client for Postman Echo endpoints."""

    BASE_URL = "https://postman-echo.com"

    def echo_get(self, params: dict):
        """Send a GET request to the /get endpoint.
        
        Requires a dictionary of query parameters to be sent.
        """
        return self.get("/get", params=params)

    def echo_post(self, payload: dict):
        """Send a POST request to the /post endpoint.
        
        Requires a JSON payload to be sent in the request body.
        """
        return self.post("/post", json=payload)

    def basic_auth(self):
        """Send GET request to the /basic-auth endpoint.
        
        Requires Basic Authentication credentials to be set in the session.
        """
        return self.get("/basic-auth")
