"""
Page Object for the Myntra shopping bag (cart) screen.

Purpose: Bag screen visibility, Place Order, empty state, and remove-item actions.
Role: Used to verify cart opens, quantity/Place Order, and empty cart after remove.
Architecture: Inherits BasePage; uses BagPageLocators.
"""
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from pages.locators import BagPageLocators
from utils.logger import logger


class BagPage(BasePage):
    """
    Shopping bag screen: items, quantity, Place Order, remove, empty state.

    Provides is_bag_screen_visible, is_place_order_visible, is_empty_bag_visible,
    has_items, remove_first_item, and is_bag_empty.
    """

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        self.locators = BagPageLocators()

    def is_bag_screen_visible(self, timeout: int = 3) -> bool:
        """Return True if the bag/cart screen is visible (items, Place Order, or title)."""
        indicators = [
            self.locators.BAG_ITEMS,
            self.locators.QTY_DROPDOWN,
            self.locators.PLACE_ORDER_BUTTON,
            self.locators.BAG_SCREEN_TITLE,
            self.locators.BAG_SCREEN_ITEMS_SELECTED,
        ]
        for loc in indicators:
            if self.is_element_present(loc, timeout=timeout):
                return True
        return False

    def is_place_order_visible(self, timeout: int = 1) -> bool:
        """Return True if the Place Order button is visible on the bag screen."""
        return self.is_element_present(self.locators.PLACE_ORDER_BUTTON, timeout=timeout)

    def is_empty_bag_visible(self, timeout: int = 2) -> bool:
        """Return True when the bag is empty (empty message or Place Order no longer visible)."""
        if self.is_element_present(self.locators.EMPTY_BAG_MESSAGE, timeout=timeout):
            return True
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(self.locators.PLACE_ORDER_BUTTON)
            )
            return True
        except Exception:
            pass
        return False

    def has_items(self) -> bool:
        """Return True if the bag contains at least one item."""
        return self.is_element_present(self.locators.BAG_ITEMS, timeout=5)

    def remove_first_item(self) -> bool:
        """Remove the first item from the bag and confirm if a dialog appears."""
        if not self.has_items():
            logger.warning("Bag is empty, cannot remove")
            return False
        self.tap(self.locators.REMOVE_ITEM)
        if self.is_element_present(self.locators.CONFIRM_REMOVE, timeout=3):
            self.tap(self.locators.CONFIRM_REMOVE)
        logger.info("Removed item from bag")
        return True

    def is_bag_empty(self) -> bool:
        """Return True if the bag is empty (empty message or no items)."""
        return self.is_element_present(self.locators.EMPTY_BAG_MESSAGE, timeout=3) or not self.has_items()
