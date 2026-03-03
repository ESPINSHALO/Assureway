"""Test: Verify home screen loads."""
import pytest
from pages import HomePage
from utils.logger import logger


@pytest.mark.smoke
def test_home_screen_loads(app_launched):
    """Verify home screen loads with key elements."""
    home = HomePage(app_launched)
    assert home.is_home_loaded(), "Home screen did not load"
    logger.info("✅ Home screen loads with search icon visible")


@pytest.mark.smoke
def test_tap_search_icon(app_launched, home_page):
    """Verify search icon is tappable."""
    result = home_page.tap_search()
    assert result, "Failed to tap search icon"
    logger.info("✅ Search icon tap successful")
