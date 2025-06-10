"""Pytest shared fixtures"""

from __future__ import annotations

import os
import pytest
from shutil import copyfile

# Conftest also runs all fixtures, so import any organized into other files
from fixtures.fixtures_browser import driver  # noqa: F401

import logging
logger = logging.getLogger()

os.environ["WDM_LOCAL"] = "1"
os.environ["WDM_CACHE_DIR"] = os.path.abspath("drivers_cache")

# Enforce script launcher:
# This repo is not intended to be used with raw pytest commands.
if "RUN_TIMESTAMP" not in os.environ:
    raise RuntimeError(
        "Please use the provided script to run tests, not pytest directly."
        "\n  `poetry run test`"
    )

def pytest_collection_modifyitems(config, items):
    """Pytest hook to skip tests based on user configurations"""
    skip = pytest.mark.skip(reason="Skipping tests that require secrets")
    for item in items:
        if "secrets" in item.keywords:
            if os.getenv("SKIP_SECRETS", "true").lower() == "true":
                item.add_marker(skip)

    # Log the collection status
    logger.info(f"Found {len(items)} test items.")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture screenshots on test failure and attach to HTML report."""
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver")
        if driver is not None:
            LATEST_SCREENSHOT_DIR = os.environ["LATEST_SCREENSHOT_DIR"]

            file_name = (
                f"{item.nodeid.replace('::', '_').replace('/', '_')}.png"
            )
            latest_screenshot_path = os.path.join(
                LATEST_SCREENSHOT_DIR,
                file_name
            )

            driver.save_screenshot(latest_screenshot_path)

            if os.getenv("SAVE_HISTORICAL_REPORTS", "false").lower() == "true":
                
                TIMESTAMPED_SCREENSHOT_DIR = os.environ[
                    "TIMESTAMPED_SCREENSHOT_DIR"
                ]
                archived_path = os.path.join(
                    TIMESTAMPED_SCREENSHOT_DIR,
                    file_name
                )
                copyfile(latest_screenshot_path, archived_path)

            if item.config.pluginmanager.hasplugin("html"):
                from pytest_html import extras
                extra = getattr(rep, "extra", [])
                extra.append(extras.image(latest_screenshot_path))
                rep.extra = extra

def pytest_configure(config):
    """Pytest hook to configure pytest settings"""
    pass

def pytest_addoption(parser):
    """Space for adding custom command line options for pytest"""
    pass
