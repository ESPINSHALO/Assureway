"""Product detail page interactions for Myntra app."""
from appium.webdriver.webdriver import WebDriver
from pages.base_page import BasePage
from pages.locators import ProductPageLocators
from utils.logger import logger


class ProductPage(BasePage):
    """Product detail page object."""

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        self.locators = ProductPageLocators()

    def select_size_if_required(self) -> bool:
        """
        Select size if size selector is present.
        Returns True if size was selected or not required.
        """
        if self.is_element_present(self.locators.SIZE_BUTTON):
            self.tap(self.locators.SIZE_BUTTON)
            if self.is_element_present(self.locators.SIZE_OPTION, timeout=5):
                return self.tap(self.locators.SIZE_OPTION)
        return True  # Size not required

    def add_to_bag(self) -> bool:
        """Tap Add to Bag button."""
        logger.info("Adding product to bag")
        return self.tap(self.locators.ADD_TO_BAG)

    def go_to_bag(self) -> bool:
        """Tap Go to Bag after adding item."""
        if self.is_element_present(self.locators.GO_TO_BAG, timeout=5):
            return self.tap(self.locators.GO_TO_BAG)
        return False
