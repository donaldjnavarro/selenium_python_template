# api_models/base_api.py
from __future__ import annotations
import requests

class BaseAPI:
    """Base class for API interactions using requests.Session."""
    
    BASE_URL: str = ""

    def __init__(self):
        """Initialize the BaseAPI with a requests session."""
        self.session = requests.Session()

    def get(self, path: str, **kwargs):
        """Send a GET request to the specified path."""
        return self.session.get(self.BASE_URL + path, **kwargs)

    def post(self, path: str, **kwargs):
        """Send a POST request to the specified path."""
        return self.session.post(self.BASE_URL + path, **kwargs)

    def with_auth(self, username: str, password: str):
        """Set HTTP Basic Auth for the session."""
        self.session.auth = requests.auth.HTTPBasicAuth(username, password)
        return self