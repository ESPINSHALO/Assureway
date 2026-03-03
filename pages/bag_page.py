"""Shopping bag page interactions for Myntra app."""
from appium.webdriver.webdriver import WebDriver
from pages.base_page import BasePage
from pages.locators import BagPageLocators
from utils.logger import logger


class BagPage(BasePage):
    """Shopping bag page object."""

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        self.locators = BagPageLocators()

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
