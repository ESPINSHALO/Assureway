"""
Single end-to-end test covering the full user journey in one driver session.

Purpose: Validate the complete flow from popup handling through search, filters, add to bag,
  cart, Place Order, back from login, remove item, and return to home.
Role: One test, one session; no per-step test isolation; used for full regression or smoke.
Architecture: Uses driver and popup_handler fixtures; script helpers for flows; HomePage for assertions.
"""
import time
import pytest

from config.capabilities import APP_PACKAGE
from pages import HomePage
from scripts.open_myntra_home import (
    perform_search,
    sort_price_low_to_high_and_open_first_shoe,
    add_to_bag_select_available_size,
    open_cart_increase_quantity_and_checkout,
)
from utils.logger import logger


@pytest.mark.regression
def test_full_e2e_flow(driver, popup_handler):
    """
    Run the full user journey: popups → search → filters → add to bag → cart → Place Order →
    back from login → open cart → remove item → return to home. Asserts home at the end.
    """
    start_time = time.time()

    # 1. Initial popup handling — ensure app has focus, wait for first screen, then Back
    try:
        driver.activate_app(APP_PACKAGE)
    except Exception:
        pass
    time.sleep(4)
    try:
        driver.back()
    except Exception:
        try:
            driver.press_keycode(4)
        except Exception:
            pass
    time.sleep(0.5)

    home_page = HomePage(driver)
    on_home = home_page.wait_until_home_visible(timeout=10)
    if not on_home:
        try:
            popup_handler.dismiss_popup()
            time.sleep(0.5)
        except Exception:
            pass
        on_home = home_page.wait_until_home_visible(timeout=6)
    assert on_home, "Expected home screen (search bar or Home tab) before starting search flow"

    # 2. Search bar finding and search list
    perform_search(driver, "shoes")

    # 3. Gender, sorting, Discounts section → open first product
    sort_price_low_to_high_and_open_first_shoe(driver, select_male=True)
    time.sleep(0.5)

    # 4. Add to bag, select size, add to bag successfully
    add_to_bag_select_available_size(driver)
    time.sleep(0.15)

    # 5–8. Return home → open cart → quantity 2 → Place Order → back from login → open cart → remove → home
    open_cart_increase_quantity_and_checkout(driver, quantity=2)

    # 9. Assert we are back on home
    assert home_page.is_home_loaded(timeout=8), "Expected to be on home screen after full E2E flow"
    logger.info("Full E2E flow completed; returned to home screen")
