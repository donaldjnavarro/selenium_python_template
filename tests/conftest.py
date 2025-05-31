"""Pytest shared fixtures"""

from __future__ import annotations

import logging
import os

import pytest
from dotenv import load_dotenv

# Conftest also runs all fixtures, so import any organized into other files
from fixtures.fixtures_browser import driver  # noqa: F401
from fixtures.fixtures_logging import pytest_configure  # noqa: F401

os.environ["WDM_LOCAL"] = "1"
os.environ["WDM_CACHE_DIR"] = os.path.abspath("drivers_cache")

# Load .env file
load_dotenv()

# Load logger
logger = logging.getLogger(__name__)

def pytest_addoption(parser):
    """Space for adding custom command line options for pytest"""
    pass

def pytest_collection_modifyitems(config, items):
    """Pytest hook to skip tests based on user configurations"""
    skip = pytest.mark.skip(reason="Skipping tests that require secrets")
    for item in items:
        if "secrets" in item.keywords:
            if os.getenv("SKIP_SECRETS", "true").lower() == "true":
                item.add_marker(skip)

    # Log the collection status
    logger.info(f"Modified {len(items)} test items.")
