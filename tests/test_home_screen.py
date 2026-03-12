"""
Tests for the home screen after app launch and popup handling.

Purpose: Validate that the home screen loads and that the search icon is tappable.
Role: Runs after app_launch tests; uses app_launched fixture to reach home.
Architecture: Uses HomePage only; no locators in this file.
"""
import time
import pytest
from pages import HomePage
from utils.logger import logger


@pytest.mark.smoke
def test_home_screen_loads(app_launched):
    """Verify that the home screen loads and key elements (search bar or Home tab) are visible."""
    time.sleep(1.0)
    home = HomePage(app_launched)
    assert home.is_home_loaded(), "Home screen did not load (search bar or Home tab not visible)"
    logger.info("✅ Home screen loads with search icon visible")


@pytest.mark.smoke
def test_tap_search_icon(app_launched, home_page):
    """Verify that the search icon is tappable and opens the search interface."""
    assert home_page.is_home_loaded(timeout=6), "Home not loaded before tap search"
    time.sleep(0.4)
    result = home_page.tap_search()
    assert result, "Failed to tap search icon"
    logger.info("✅ Search icon tap successful")
