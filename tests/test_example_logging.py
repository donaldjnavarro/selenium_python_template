from __future__ import annotations

import logging
import pytest

# Create the logger
logger = logging.getLogger(__name__)

@pytest.mark.example
def test_logging_example():
    """Test to check if logging works"""
    # logger
    logger.debug("This is an example logger.debug() log")
    logger.info("This is an example logger.info() log")
    logger.warning("This is an example logger.warning() log")
    logger.critical("This is an example logger.critical() log")
    # print
    print("This is an example print() message")
    assert True