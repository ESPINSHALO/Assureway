"""
Tests for the search flow: search, filters (Gender, Sort), open product, add to bag.

Purpose: Validate search, listing filters, first product open, and add-to-bag with size selection.
Role: Uses app_launched and script helpers (perform_search, select_gender_male, etc.); asserts via page objects.
Architecture: No locators in tests; visibility checks use search_page and product_page methods.
"""
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
    """Verify that a user can search for a product and the listing page (SORT/GENDER visible) is displayed."""
    try:
        perform_search(app_launched, "shoes")
    except Exception as e:
        raise AssertionError(f"Search failed - cannot validate results: {e}") from e
    time.sleep(2)
    assert search_page.is_listing_visible(timeout=5), (
        "Search listing did not display (SORT/GENDER not found)"
    )
    logger.info("✅ Search flow completed - listing displayed")


@pytest.mark.regression
def test_gender_select_male(app_launched, home_page, search_page):
    """Verify that on the listing page the user can open Gender and select Male."""
    try:
        perform_search(app_launched, "shoes")
    except Exception as e:
        raise AssertionError(f"Search failed - cannot test Gender: {e}") from e
    time.sleep(2)
    assert select_gender_male(app_launched), "Failed to click Gender and select Male"
    logger.info("✅ Gender → Male selected")


@pytest.mark.regression
def test_sort_select_discounts(app_launched, home_page, search_page):
    """Verify that on the listing page the user can open Sort and select Discounts."""
    try:
        perform_search(app_launched, "shoes")
    except Exception as e:
        raise AssertionError(f"Search failed - cannot test Sort: {e}") from e
    time.sleep(2)
    assert select_gender_male(app_launched), "Failed to select Gender Male first"
    time.sleep(0.5)
    assert select_sort_discounts(app_launched), "Failed to click Sort and select Discounts"
    logger.info("✅ Sort → Discounts selected")


@pytest.mark.regression
def test_open_first_product(app_launched, home_page, search_page, product_page):
    """Verify that from the listing (after Gender and Sort) the first product opens and the product details page loads."""
    try:
        perform_search(app_launched, "shoes")
    except Exception as e:
        raise AssertionError(f"Search failed - cannot open product: {e}") from e
    time.sleep(2)
    assert select_gender_male(app_launched), "Failed to select Gender Male"
    assert select_sort_discounts(app_launched), "Failed to select Sort Discounts"
    assert open_first_listing_product(app_launched), "Failed to open first product"
    time.sleep(2.5)
    product_visible = product_page.is_product_page_visible(timeout=4) or search_page.is_listing_gone(timeout=1)
    assert product_visible, (
        "Product details page did not load (Add to bag / Size not found or listing still visible)"
    )
    logger.info("✅ First product opened - product details page loaded")


@pytest.mark.regression
def test_select_size_and_add_to_bag(app_launched, home_page, search_page, product_page):
    """Verify that on the product page the user can select a size, add to bag, and see Go to bag or DONE confirmation."""
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
    assert product_page.is_go_to_bag_or_add_success(timeout=6), (
        "Add to bag did not complete (Go to bag not found and size popup still visible)"
    )
    logger.info("✅ Selected size and added to bag - Go to bag visible or DONE confirmed")
