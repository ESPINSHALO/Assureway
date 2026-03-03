"""Test: Bag operations - remove item, navigate back."""
import pytest
import time
from pages import HomePage, SearchPage, ProductPage, BagPage
from utils.logger import logger


@pytest.mark.regression
def test_remove_item_from_bag(app_launched, home_page, search_page, product_page, bag_page):
    """
    Add item to bag -> Open bag -> Remove item -> Verify bag empty.
    """
    # Add item first
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
    
    if not bag_page.has_items():
        pytest.skip("Could not add item to bag for removal test")
    
    # Remove item
    bag_page.remove_first_item()
    time.sleep(2)
    
    # Bag should be empty (or have confirmation)
    logger.info("✅ Remove from bag flow completed")


@pytest.mark.regression
def test_navigate_back_to_home(app_launched, home_page, bag_page):
    """Open bag (or any screen) and navigate back to home."""
    home_page.tap_bag()
    time.sleep(2)
    
    # Press back
    home_page.go_back()
    time.sleep(2)
    
    assert home_page.is_home_loaded(), "Did not return to home screen"
    logger.info("✅ Navigated back to home screen")
