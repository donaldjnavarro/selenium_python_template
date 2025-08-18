"""Pytest shared fixtures"""

from __future__ import annotations

import os
import pytest
from shutil import copyfile
import logging
from fixtures.fixtures_browser import driver  # noqa: F401

logger = logging.getLogger()

# Enforce script launcher:
if "RUN_TIMESTAMP" not in os.environ:
    raise RuntimeError(
        "Please use the provided script to run tests, not pytest directly."
        "\n  `poetry run test`"
    )


def pytest_collection_modifyitems(config, items):
    """Skip tests that require secrets if SKIP_SECRETS is True"""
    skip = pytest.mark.skip(reason="Skipping tests that require secrets")
    for item in items:
        if "secrets" in item.keywords and os.getenv("SKIP_SECRETS", "true").lower() == "true":
            item.add_marker(skip)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture screenshots on test failure for session-scoped drivers"""
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver")
        if driver:
            latest_dir = os.environ["LATEST_SCREENSHOT_DIR"]
            file_name = f"{item.nodeid.replace('::', '_').replace('/', '_')}.png"
            latest_path = os.path.join(latest_dir, file_name)

            driver.save_screenshot(latest_path)

            if os.getenv("SAVE_HISTORICAL_REPORTS", "false").lower() == "true":
                timestamped_dir = os.environ["TIMESTAMPED_SCREENSHOT_DIR"]
                archived_path = os.path.join(timestamped_dir, file_name)
                copyfile(latest_path, archived_path)

            if item.config.pluginmanager.hasplugin("html"):
                from pytest_html import extras
                extra = getattr(rep, "extra", [])
                extra.append(extras.image(latest_path))
                rep.extra = extra


def pytest_runtest_setup(item):
    """Log before each test starts"""
    logger.info(f"Starting test: {item.nodeid}")

def pytest_runtest_teardown(item, nextitem):
    """Log after each test finishes"""
    logger.info(f"Finished test: {item.nodeid}")

