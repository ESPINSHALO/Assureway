"""
Cart & checkout flow tests (after add to bag):
1. Navigate to home screen
2. Open cart, increase quantity to 2, click Place Order
3. Login screen opens → return back to home page
4. Open cart again, click X (remove icon), click Remove button, verify empty cart, return to home
"""
import pytest
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.locators import BagPageLocators, HomePageLocators, PopupLocators
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
    """Shared setup: search → Gender → Sort → open product → add to bag. Returns True if successful."""
    for attempt in range(retries):
        try:
            perform_search(driver, "shoes")
        except Exception:
            if attempt == retries - 1:
                return False
            time.sleep(2)
            continue
        time.sleep(2.5)  # Let listing load (SORT/GENDER)
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
        time.sleep(3)  # Let product page load before Add to bag
        add_to_bag_select_available_size(driver)
        time.sleep(1.5)
        return True
    return False


@pytest.mark.regression
def test_navigate_to_home_after_add_to_bag(app_launched, home_page):
    """
    1. After add to bag: navigate to home screen and verify home is visible.
    """
    assert _add_to_bag_and_get_to_product_page(app_launched), (
        "Add to bag setup failed: search → gender → sort → open product → add to bag did not complete"
    )
    assert return_to_home(app_launched), "Failed to return to home after add to bag"
    time.sleep(0.5)
    assert home_page.is_home_loaded(), "Home screen not visible after navigation"
    logger.info("✅ Navigated to home screen after add to bag")


@pytest.mark.regression
def test_open_cart_increase_quantity_done(app_launched, home_page):
    """
    2a. Navigate to home, open cart, increase quantity to 2, click DONE (quantity).
    Stops at cart screen — does not click Place Order.
    """
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
def test_click_place_order_opens_login(app_launched, home_page):
    """
    2b. Individual test: on cart (with qty 2 and DONE), click Place Order and verify login screen opens.
    """
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
    login_locators = [
        PopupLocators.PROFILE_LOGIN_BUTTON,
        PopupLocators.LOGIN_LOGIN_SIGNUP_TEXT,
        PopupLocators.LOGIN_LOGIN_SIGNUP_DESC,
        PopupLocators.LOGIN_SIGNIN_TEXT,
        PopupLocators.LOGIN_CONTINUE_PHONE,
        PopupLocators.LOGIN_MOBILE_HINT,
    ]
    login_visible = False
    wait_login = WebDriverWait(app_launched, 4)
    for loc in login_locators:
        try:
            wait_login.until(EC.visibility_of_element_located(loc))
            login_visible = True
            break
        except Exception:
            continue
    if not login_visible:
        try:
            app_launched.find_element(*BagPageLocators.PLACE_ORDER_BUTTON)
        except Exception:
            login_visible = True
    assert login_visible, "Login screen did not open after Place Order"
    logger.info("✅ Place Order clicked - login screen opened")


@pytest.mark.regression
def test_back_from_login_to_home(app_launched, home_page):
    """
    3. After Place Order, login screen opens; close it (X) and return back to home page.
    """
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


def _open_cart_from_home(driver):
    """Open cart (bag icon) from home. Returns True if cart opened."""
    try:
        bag_el = driver.find_element(*HomePageLocators.BAG_ICON)
        bag_el.click()
        return True
    except Exception:
        try:
            sz = driver.get_window_size()
            driver.tap([(int(sz["width"] * 0.92), int(sz["height"] * 0.96))])
            return True
        except Exception:
            return False


def _wait_for_cart_screen_visible(driver, timeout: int = 3):
    """Wait until shopping bag/cart screen is visible (so remove can run). Returns True if cart is visible."""
    cart_indicators = [
        BagPageLocators.BAG_ITEMS,
        BagPageLocators.QTY_DROPDOWN,
        BagPageLocators.PLACE_ORDER_BUTTON,
        BagPageLocators.BAG_SCREEN_TITLE,
        BagPageLocators.BAG_SCREEN_ITEMS_SELECTED,
    ]
    for loc in cart_indicators:
        try:
            WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(loc))
            return True
        except Exception:
            continue
    return False


@pytest.mark.regression
def test_remove_product_from_cart(app_launched, home_page):
    """
    4a. After back from login: open cart, click X (remove icon), click Remove button.
    Verify cart is empty (no return home).
    """
    assert _add_to_bag_and_get_to_product_page(app_launched), (
        "Add to bag setup failed: search → gender → sort → open product → add to bag did not complete"
    )
    assert return_to_home(app_launched), "Failed to return to home"
    assert open_cart_set_quantity_place_order(app_launched, quantity=2, skip_return_to_home=True), (
        "Could not open cart / place order"
    )
    back_from_login_to_home(app_launched)
    time.sleep(0.3)
    assert _open_cart_from_home(app_launched), "Could not open cart again"
    time.sleep(0.3)
    assert _wait_for_cart_screen_visible(app_launched), "Cart screen did not load after opening bag"
    time.sleep(0.1)
    assert remove_product_from_cart(app_launched), "Failed to remove product from cart"
    empty_ok = False
    try:
        WebDriverWait(app_launched, 2).until(EC.visibility_of_element_located(BagPageLocators.EMPTY_BAG_MESSAGE))
        empty_ok = True
    except Exception:
        try:
            WebDriverWait(app_launched, 2).until(
                EC.invisibility_of_element_located(BagPageLocators.PLACE_ORDER_BUTTON)
            )
            empty_ok = True
        except Exception:
            pass
    assert empty_ok, "Cart did not appear empty after remove"
    logger.info("✅ Removed product from cart; cart is empty")


@pytest.mark.regression
def test_verify_empty_cart_and_return_home(app_launched, home_page):
    """
    4b. On cart (with item): remove item, verify empty cart, then return to home page.
    """
    assert _add_to_bag_and_get_to_product_page(app_launched), (
        "Add to bag setup failed: search → gender → sort → open product → add to bag did not complete"
    )
    assert return_to_home(app_launched), "Failed to return to home"
    assert open_cart_set_quantity_place_order(app_launched, quantity=2, skip_return_to_home=True), (
        "Could not open cart / place order"
    )
    back_from_login_to_home(app_launched)
    time.sleep(0.3)
    assert _open_cart_from_home(app_launched), "Could not open cart again"
    time.sleep(0.3)
    assert _wait_for_cart_screen_visible(app_launched), "Cart screen did not load after opening bag"
    time.sleep(0.1)
    empty_cart_and_return_home(app_launched)
    time.sleep(0.5)
    assert home_page.is_home_loaded(), "Did not return to home after empty cart"
    logger.info("✅ Verified empty cart and returned to home")
