from __future__ import annotations

import pytest

import logging
logger = logging.getLogger()


@pytest.mark.example
def test_logging_example():
    """Test to check if logging works"""
    # logger    
    logger.debug("This is an example logger.debug() log within a test")
    logger.info("This is an example logger.info() log within a test")
    logger.warning("This is an example logger.warning() log within a test")
    logger.critical("This is an example logger.critical() log within a test")
    # print
    print("This is an example print() message within a test")
    assert True
