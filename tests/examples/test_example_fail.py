"""Test forces a fail to verify failure handling"""
from __future__ import annotations
import pytest

@pytest.mark.fail(reason="Test intentionally fails to verify failure handling")
def test_fail_example(driver):
    driver.get("https://example.com")
    assert False, "Intentional failure to test failure handling in pytest"