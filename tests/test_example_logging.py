from __future__ import annotations

import logging
import pytest

# Create the logger
logger = logging.getLogger(__name__)

@pytest.mark.example
def test_logging_example():
    """Test to check if logging works"""
    # logger
    logger.debug("This is a debug log message")
    logger.info("This is an info log message")
    logger.warning("This is a warning log message")
    logger.critical("This is a critical log message")
    # print
    print("This is a print message")
    assert True