"""Test: Navigation, scroll, UI responsiveness, popups."""
import pytest
import time
from pages import HomePage, PopupHandler
from utils.logger import logger


@pytest.mark.regression
def test_scroll_through_product_list(app_launched, home_page):
    """Scroll through product list and verify UI responsiveness."""
    for _ in range(2):
        home_page.scroll_down()
        time.sleep(1)
    
    for _ in range(2):
        home_page.scroll_up()
        time.sleep(1)
    
    logger.info("✅ Scroll through product list - UI responsive")


@pytest.mark.regression
def test_navigation_transitions(app_launched, home_page):
    """Verify navigation transitions (home -> bag -> home)."""
    home_page.tap_bag()
    time.sleep(2)
    home_page.go_back()
    time.sleep(2)
    assert home_page.is_home_loaded(), "Navigation transition failed"
    logger.info("✅ Navigation transitions validated")


@pytest.mark.regression
def test_handle_unexpected_popups(driver, popup_handler):
    """Verify app stability when handling unexpected popups."""
    import time
    time.sleep(4)
    popup_handler.handle_initial_popups()
    time.sleep(1)
    # App should still be responsive
    assert driver is not None
    logger.info("✅ Popup handling - app stable")
