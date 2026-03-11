"""Shopping bag page interactions for Myntra app."""
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from pages.locators import BagPageLocators
from utils.logger import logger


class BagPage(BasePage):
    """Shopping bag page object."""

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        self.locators = BagPageLocators()

    def is_bag_screen_visible(self, timeout: int = 3) -> bool:
        """True if bag/cart screen is visible (items, Place Order, title, etc.)."""
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
        """True if Place Order button is visible (still on bag screen)."""
        return self.is_element_present(self.locators.PLACE_ORDER_BUTTON, timeout=timeout)

    def is_empty_bag_visible(self, timeout: int = 2) -> bool:
        """True if bag is empty (empty message visible or Place Order gone)."""
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
        """Check if bag has any items."""
        return self.is_element_present(self.locators.BAG_ITEMS, timeout=5)

    def remove_first_item(self) -> bool:
        """Remove first item from bag."""
        if not self.has_items():
            logger.warning("Bag is empty, cannot remove")
            return False
        self.tap(self.locators.REMOVE_ITEM)
        if self.is_element_present(self.locators.CONFIRM_REMOVE, timeout=3):
            self.tap(self.locators.CONFIRM_REMOVE)
        logger.info("Removed item from bag")
        return True

    def is_bag_empty(self) -> bool:
        """Check if bag is empty."""
        return self.is_element_present(self.locators.EMPTY_BAG_MESSAGE, timeout=3) or not self.has_items()
