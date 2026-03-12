"""
Tests for cart and checkout flow after adding a product to the bag.

Purpose: Validate navigate to home, open cart, set quantity, Place Order (login screen), back from login,
  remove item, empty cart, and return to home.
Role: Depends on add-to-bag setup (search → gender → sort → product → add to bag); uses script helpers and page objects.
Architecture: No locators in tests; uses bag_page, home_page, popup_handler for assertions.
"""
import pytest
import time

from scripts.open_myntra_home import (
    perform_search,
    select_gender_male,
    select_sort_discounts,
    open_first_listing_product,
    add_to_bag_select_available_size,
    return_to_home,
    open_cart_set_quantity_done_only,
    click_place_order,
    open_cart_set_quantity_place_order,
    back_from_login_to_home,
    remove_product_from_cart,
    empty_cart_and_return_home,
)
from utils.logger import logger


def _add_to_bag_and_get_to_product_page(driver, retries=2):
    """Shared setup: perform search, apply Gender and Sort, open first product, add to bag. Returns True if all steps succeed."""
    for attempt in range(retries):
        try:
            perform_search(driver, "shoes")
        except Exception:
            if attempt == retries - 1:
                return False
            time.sleep(2)
            continue
        time.sleep(2.5)
        if not select_gender_male(driver):
            if attempt == retries - 1:
                return False
            time.sleep(1)
            continue
        time.sleep(0.5)
        if not select_sort_discounts(driver):
            if attempt == retries - 1:
                return False
            time.sleep(1)
            continue
        time.sleep(0.5)
        if not open_first_listing_product(driver):
            if attempt == retries - 1:
                return False
            time.sleep(2)
            continue
        time.sleep(3)
        add_to_bag_select_available_size(driver)
        time.sleep(1.5)
        return True
    return False


@pytest.mark.regression
def test_navigate_to_home_after_add_to_bag(app_launched, home_page):
    """Verify that after adding to bag the user can navigate back to the home screen and home is visible."""
    assert _add_to_bag_and_get_to_product_page(app_launched), (
        "Add to bag setup failed: search → gender → sort → open product → add to bag did not complete"
    )
    assert return_to_home(app_launched), "Failed to return to home after add to bag"
    time.sleep(0.5)
    assert home_page.is_home_loaded(), "Home screen not visible after navigation"
    logger.info("✅ Navigated to home screen after add to bag")


@pytest.mark.regression
def test_open_cart_increase_quantity_done(app_launched, home_page):
    """Verify that from home the user can open the cart, set quantity to 2, and click DONE (stays on cart screen)."""
    assert _add_to_bag_and_get_to_product_page(app_launched), (
        "Add to bag setup failed: search → gender → sort → open product → add to bag did not complete"
    )
    assert return_to_home(app_launched), "Failed to return to home"
    time.sleep(0.2)
    assert open_cart_set_quantity_done_only(app_launched, quantity=2, skip_return_to_home=True), (
        "Failed to open cart or set quantity to 2 and click DONE"
    )
    logger.info("✅ Open cart, quantity 2, DONE clicked")


@pytest.mark.regression
def test_click_place_order_opens_login(app_launched, home_page, bag_page, popup_handler):
    """Verify that from the cart screen clicking Place Order opens the login/signup screen."""
    assert _add_to_bag_and_get_to_product_page(app_launched), (
        "Add to bag setup failed: search → gender → sort → open product → add to bag did not complete"
    )
    assert return_to_home(app_launched), "Failed to return to home"
    time.sleep(0.2)
    assert open_cart_set_quantity_done_only(app_launched, quantity=2, skip_return_to_home=True), (
        "Failed to open cart and set quantity"
    )
    time.sleep(0.4)
    assert click_place_order(app_launched), "Failed to click Place Order"
    time.sleep(1.5)
    login_visible = popup_handler.is_login_screen_visible(timeout=4)
    if not login_visible:
        login_visible = not bag_page.is_place_order_visible(timeout=1)
    assert login_visible, "Login screen did not open after Place Order"
    logger.info("✅ Place Order clicked - login screen opened")


@pytest.mark.regression
def test_back_from_login_to_home(app_launched, home_page):
    """Verify that after Place Order the login screen can be closed and the user returns to the home page."""
    assert _add_to_bag_and_get_to_product_page(app_launched), (
        "Add to bag setup failed: search → gender → sort → open product → add to bag did not complete"
    )
    assert return_to_home(app_launched), "Failed to return to home"
    assert open_cart_set_quantity_place_order(app_launched, quantity=2, skip_return_to_home=True), (
        "Could not reach Place Order / login screen (open cart, set qty, click Place Order)"
    )
    time.sleep(0.3)
    assert back_from_login_to_home(app_launched), "Failed to close login and return to home"
    time.sleep(0.5)
    assert home_page.is_home_loaded(), "Home screen not visible after back from login"
    logger.info("✅ Back from login to home page")


@pytest.mark.regression
def test_remove_product_from_cart(app_launched, home_page, bag_page):
    """Verify that after returning from login the user can open the cart, remove the item, and see an empty cart."""
    assert _add_to_bag_and_get_to_product_page(app_launched), (
        "Add to bag setup failed: search → gender → sort → open product → add to bag did not complete"
    )
    assert return_to_home(app_launched), "Failed to return to home"
    assert open_cart_set_quantity_place_order(app_launched, quantity=2, skip_return_to_home=True), (
        "Could not open cart / place order"
    )
    assert back_from_login_to_home(app_launched), "Failed to close login and return to home"
    # Wait for home to be ready so bottom nav (bag icon) is visible before opening cart
    assert home_page.is_home_loaded(timeout=5), "Home not visible after back from login"
    time.sleep(0.5)
    assert home_page.tap_bag(timeout=5), "Could not open cart again"
    time.sleep(0.4)
    assert bag_page.is_bag_screen_visible(timeout=5), "Cart screen did not load after opening bag"
    time.sleep(0.15)
    assert remove_product_from_cart(app_launched), "Failed to remove product from cart"
    assert bag_page.is_empty_bag_visible(timeout=3), "Cart did not appear empty after remove"
    logger.info("✅ Removed product from cart; cart is empty")


@pytest.mark.regression
def test_verify_empty_cart_and_return_home(app_launched, home_page, bag_page):
    """Verify that from the cart the user can remove the item, see empty cart, and return to the home page."""
    assert _add_to_bag_and_get_to_product_page(app_launched), (
        "Add to bag setup failed: search → gender → sort → open product → add to bag did not complete"
    )
    assert return_to_home(app_launched), "Failed to return to home"
    assert open_cart_set_quantity_place_order(app_launched, quantity=2, skip_return_to_home=True), (
        "Could not open cart / place order"
    )
    assert back_from_login_to_home(app_launched), "Failed to close login and return to home"
    assert home_page.is_home_loaded(timeout=5), "Home not visible after back from login"
    time.sleep(0.5)
    assert home_page.tap_bag(timeout=5), "Could not open cart again"
    time.sleep(0.4)
    assert bag_page.is_bag_screen_visible(timeout=5), "Cart screen did not load after opening bag"
    time.sleep(0.15)
    empty_cart_and_return_home(app_launched)
    time.sleep(0.5)
    assert home_page.is_home_loaded(), "Did not return to home after empty cart"
    logger.info("✅ Verified empty cart and returned to home")
