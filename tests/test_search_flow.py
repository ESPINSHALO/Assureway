"""Test: Search flow - tap search, search product, validate results."""
import pytest
import time
from pages import HomePage, SearchPage
from utils.logger import logger


@pytest.mark.regression
def test_search_for_product(app_launched, home_page, search_page):
    """
    Tap search icon, search for 'shoes', validate search results display.
    """
    # Tap search
    assert home_page.tap_search(), "Failed to tap search icon"
    time.sleep(2)
    
    # Enter search term
    assert search_page.enter_search_term("shoes"), "Failed to enter search"
    time.sleep(5)  # Wait for results to load
    
    # Validate results
    assert search_page.has_results(), "Search results did not display"
    logger.info("✅ Search flow completed - results displayed")


@pytest.mark.regression
def test_open_product_from_results(app_launched, home_page, search_page, product_page):
    """
    Search for product, open first result, verify product details page loads.
    """
    home_page.tap_search()
    time.sleep(2)
    search_page.enter_search_term("shoes")
    time.sleep(5)
    
    assert search_page.has_results(), "No search results"
    search_page.tap_first_result()
    time.sleep(3)
    
    # Product page should have Add to Bag or similar
    assert product_page.is_element_present(product_page.locators.ADD_TO_BAG, timeout=10) or \
           product_page.is_element_present(product_page.locators.SIZE_BUTTON, timeout=5), \
           "Product details page did not load"
    logger.info("✅ Product details page loaded")
