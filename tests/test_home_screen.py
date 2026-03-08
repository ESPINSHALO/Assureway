"""Test: Verify home screen loads (after app launch and popup handling)."""
import time
import pytest
from pages import HomePage
from utils.logger import logger


@pytest.mark.smoke
def test_home_screen_loads(app_launched):
    """Verify home screen loads with key elements (search bar / Home tab)."""
    time.sleep(1.0)  # Let home settle after app_launched
    home = HomePage(app_launched)
    # Allow up to 8s for home (search bar or Home tab) to appear; app may load slowly
    assert home.is_home_loaded(), "Home screen did not load (search bar or Home tab not visible)"
    logger.info("✅ Home screen loads with search icon visible")


@pytest.mark.smoke
def test_tap_search_icon(app_launched, home_page):
    """Verify search icon is tappable and opens search."""
    time.sleep(0.5)
    result = home_page.tap_search()
    assert result, "Failed to tap search icon"
    logger.info("✅ Search icon tap successful")
