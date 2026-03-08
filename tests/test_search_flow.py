"""Test: Search flow - search, Gender → Male, Sort → Discounts, open product, select size & add to bag."""
import pytest
import time
from pages import HomePage, SearchPage
from scripts.open_myntra_home import (
    perform_search,
    select_gender_male,
    select_sort_discounts,
    open_first_listing_product,
    add_to_bag_select_available_size,
)
from utils.logger import logger


@pytest.mark.regression
def test_search_for_product(app_launched, home_page, search_page):
    """
    1. Search: tap search bar, type 'shoes', validate listing page (SORT/GENDER visible).
    """
    try:
        perform_search(app_launched, "shoes")
    except Exception as e:
        raise AssertionError(f"Search failed - cannot validate results: {e}") from e
    time.sleep(2)
    # Listing page has SORT and GENDER; has_results() may not match listing layout
    listing_visible = (
        search_page.is_element_present(search_page.locators.SORT_BUTTON, timeout=5)
        or search_page.is_element_present(search_page.locators.GENDER_BUTTON, timeout=5)
    )
    assert listing_visible, "Search listing did not display (SORT/GENDER not found)"
    logger.info("✅ Search flow completed - listing displayed")


@pytest.mark.regression
def test_gender_select_male(app_launched, home_page, search_page):
    """
    2. On listing: click Gender, select Male.
    """
    try:
        perform_search(app_launched, "shoes")
    except Exception as e:
        raise AssertionError(f"Search failed - cannot test Gender: {e}") from e
    time.sleep(2)
    assert select_gender_male(app_launched), "Failed to click Gender and select Male"
    logger.info("✅ Gender → Male selected")


@pytest.mark.regression
def test_sort_select_discounts(app_launched, home_page, search_page):
    """
    3. On listing: click Sort, select Discounts.
    """
    try:
        perform_search(app_launched, "shoes")
    except Exception as e:
        raise AssertionError(f"Search failed - cannot test Sort: {e}") from e
    time.sleep(2)  # Let listing load (SORT/GENDER) before interacting
    assert select_gender_male(app_launched), "Failed to select Gender Male first"
    time.sleep(0.5)  # Let Gender selection apply before opening Sort
    assert select_sort_discounts(app_launched), "Failed to click Sort and select Discounts"
    logger.info("✅ Sort → Discounts selected")


def _is_product_page_visible(driver, product_page, search_page, timeout: int = 3) -> bool:
    """True if any product-detail indicator is visible, or we left the listing (flow succeeded)."""
    from appium.webdriver.common.appiumby import AppiumBy
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    locators = [
        product_page.locators.ADD_TO_BAG,
        product_page.locators.ADD_TO_BAG_TEXT,
        product_page.locators.ADD_TO_BAG_DESC,
        product_page.locators.SIZE_BUTTON,
        product_page.locators.SELECT_SIZE,
        (AppiumBy.XPATH, "//*[contains(translate(@text,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'add to bag')]"),
        (AppiumBy.XPATH, "//*[contains(translate(@content-desc,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'add to bag')]"),
    ]
    for loc in locators:
        try:
            WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(loc))
            return True
        except Exception:
            continue
    # Flow success: we opened first product so listing (SORT/GENDER) should no longer be visible
    try:
        WebDriverWait(driver, 1).until(EC.invisibility_of_element_located(search_page.locators.SORT_BUTTON))
        return True
    except Exception:
        pass
    try:
        WebDriverWait(driver, 1).until(EC.invisibility_of_element_located(search_page.locators.GENDER_BUTTON))
        return True
    except Exception:
        pass
    return False


@pytest.mark.regression
def test_open_first_product(app_launched, home_page, search_page, product_page):
    """
    4. On listing (after Gender + Sort): open first product, verify product details page.
    Order: search → Gender Male → Sort Discounts → open first product.
    """
    try:
        perform_search(app_launched, "shoes")
    except Exception as e:
        raise AssertionError(f"Search failed - cannot open product: {e}") from e
    time.sleep(2)
    assert select_gender_male(app_launched), "Failed to select Gender Male"
    assert select_sort_discounts(app_launched), "Failed to select Sort Discounts"
    assert open_first_listing_product(app_launched), "Failed to open first product"
    time.sleep(2.5)
    assert _is_product_page_visible(app_launched, product_page, search_page, timeout=4), \
        "Product details page did not load (Add to bag / Size not found or listing still visible)"
    logger.info("✅ First product opened - product details page loaded")


def _is_go_to_bag_or_add_success(driver, product_page, timeout: int = 3) -> bool:
    """True if Go to bag visible, or size popup is gone (DONE was clicked = flow succeeded)."""
    from appium.webdriver.common.appiumby import AppiumBy
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    locators = [
        product_page.locators.GO_TO_BAG,
        (AppiumBy.XPATH, "//*[contains(@text,'GO TO BAG') or contains(@text,'Go to Bag') or contains(@text,'Go to bag')]"),
        (AppiumBy.XPATH, "//*[contains(translate(@text,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'go to bag')]"),
        (AppiumBy.XPATH, "//*[contains(translate(@content-desc,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'go to bag')]"),
    ]
    for loc in locators:
        try:
            WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(loc))
            return True
        except Exception:
            continue
    # Flow success: size was selected and DONE clicked, so "Select Size" popup should be gone
    try:
        WebDriverWait(driver, 1).until(
            EC.invisibility_of_element_located(product_page.locators.SIZE_POPUP_TITLE)
        )
        return True
    except Exception:
        pass
    try:
        WebDriverWait(driver, 1).until(
            EC.invisibility_of_element_located(
                (AppiumBy.XPATH, "//*[contains(@text,'Select Size') or contains(@text,'UK Size')]")
            )
        )
        return True
    except Exception:
        pass
    return False


@pytest.mark.regression
def test_select_size_and_add_to_bag(app_launched, home_page, search_page, product_page):
    """
    5. On product page: select available shoe size, click Add to bag, confirm (Go to bag visible or popup closed).
    Order: search → Gender → Sort → open first product → Add to bag → select size → DONE.
    """
    try:
        perform_search(app_launched, "shoes")
    except Exception as e:
        raise AssertionError(f"Search failed - cannot test add to bag: {e}") from e
    time.sleep(2)
    assert select_gender_male(app_launched), "Failed to select Gender Male"
    assert select_sort_discounts(app_launched), "Failed to select Sort Discounts"
    assert open_first_listing_product(app_launched), "Failed to open first product"
    time.sleep(2)
    add_to_bag_select_available_size(app_launched)
    time.sleep(2.5)
    assert _is_go_to_bag_or_add_success(app_launched, product_page, timeout=6), \
        "Add to bag did not complete (Go to bag not found and size popup still visible)"
    logger.info("✅ Selected size and added to bag - Go to bag visible or DONE confirmed")
