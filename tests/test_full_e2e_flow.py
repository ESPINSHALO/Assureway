"""
Full E2E test: popup handling → search → gender/sort/discounts → add to bag (size) →
return home → open cart → increase quantity → place order → back from login → cart → remove → home.
"""
import time
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.locators import HomePageLocators
from scripts.open_myntra_home import (
    MYNTRA_PACKAGE,
    perform_search,
    sort_price_low_to_high_and_open_first_shoe,
    add_to_bag_select_available_size,
    open_cart_increase_quantity_and_checkout,
)
from utils.logger import logger


@pytest.mark.regression
def test_full_e2e_flow(driver, popup_handler):
    """
    Complete flow:
    1. Initial popup handling (Back once to reach home)
    2. Search bar finding and search list (type shoes)
    3. Gender, sorting, Discounts section
    4. Click first product, Add to bag, select size, add to bag successfully
    5. Return to home
    6. Open cart, increase quantity, click Place Order
    7. Back from login page to home page
    8. Click cart again, perform remove operation
    9. Return back to home
    """
    start_time = time.time()

    # 1. Initial popup handling — ensure app has focus, wait for first screen, then Back
    try:
        driver.activate_app(MYNTRA_PACKAGE)
    except Exception:
        pass
    time.sleep(4)  # Ensure splash/onboarding is visible before Back (pytest can be slower)
    try:
        driver.back()  # Prefer Appium back(); often more reliable than press_keycode(4) in tests
    except Exception:
        try:
            driver.press_keycode(4)  # KEYCODE_BACK fallback
        except Exception:
            pass
    time.sleep(0.5)
    # Wait for home (search bar or Home tab); avoid repeated popup handling that taps top-right (Profile icon)
    wait = WebDriverWait(driver, 10)
    home_locators = [
        HomePageLocators.SEARCH_CONTAINER,
        HomePageLocators.SEARCH_CONTAINER_XPATH,
        HomePageLocators.SEARCH_BAR_PLACEHOLDER,
        HomePageLocators.HOME_TAB,
        HomePageLocators.HOME_TAB_ALT,
    ]
    on_home = False
    for loc in home_locators:
        try:
            wait.until(EC.visibility_of_element_located(loc))
            on_home = True
            break
        except Exception:
            continue
    if not on_home:
        # If we landed on Profile, dismiss once (Back) then wait for home again
        try:
            popup_handler.dismiss_popup()
            time.sleep(0.5)
        except Exception:
            pass
        for loc in home_locators:
            try:
                WebDriverWait(driver, 6).until(EC.visibility_of_element_located(loc))
                on_home = True
                break
            except Exception:
                continue
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
    wait = WebDriverWait(driver, 8)
    on_home = False
    for loc in [HomePageLocators.HOME_TAB, HomePageLocators.HOME_TAB_ALT]:
        try:
            wait.until(EC.visibility_of_element_located(loc))
            on_home = True
            break
        except Exception:
            continue
    assert on_home, "Expected to be on home screen after full E2E flow"
    logger.info("Full E2E flow completed; returned to home screen")
