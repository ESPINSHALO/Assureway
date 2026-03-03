"""Test: Add to bag flow - select size, add, verify in bag."""
import pytest
import time
from pages import HomePage, SearchPage, ProductPage, BagPage
from utils.logger import logger


@pytest.mark.regression
def test_add_product_to_bag(app_launched, home_page, search_page, product_page, bag_page):
    """
    Search -> Open product -> Select size (if required) -> Add to bag -> Verify.
    """
    # Search and open product
    home_page.tap_search()
    time.sleep(2)
    search_page.enter_search_term("shoes")
    time.sleep(5)
    
    if not search_page.has_results():
        pytest.skip("No search results - cannot continue add to bag test")
    
    search_page.tap_first_result()
    time.sleep(3)
    
    # Select size if required
    product_page.select_size_if_required()
    time.sleep(1)
    
    # Add to bag
    assert product_page.add_to_bag(), "Failed to add to bag"
    time.sleep(2)
    
    # Go to bag if prompted
    product_page.go_to_bag()
    time.sleep(2)
    
    # Alternatively navigate via bag icon if go_to_bag didn't work
    if not bag_page.has_items():
        home_page.tap_bag()
        time.sleep(2)
    
    assert bag_page.has_items(), "Product was not added to bag"
    logger.info("✅ Product added to bag successfully")


@pytest.mark.regression
def test_verify_product_in_bag(app_launched, home_page, search_page, product_page, bag_page):
    """Add item and verify it appears in bag."""
    home_page.tap_search()
    time.sleep(2)
    search_page.enter_search_term("shoes")
    time.sleep(5)
    
    if not search_page.has_results():
        pytest.skip("No search results")
    
    search_page.tap_first_result()
    time.sleep(3)
    product_page.select_size_if_required()
    product_page.add_to_bag()
    time.sleep(2)
    product_page.go_to_bag()
    time.sleep(2)
    
    if not bag_page.has_items():
        home_page.tap_bag()
        time.sleep(2)
    
    assert bag_page.has_items(), "Item not found in bag"
    logger.info("✅ Product verified in bag")
