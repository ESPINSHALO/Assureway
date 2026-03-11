"""Product detail page interactions for Myntra app."""
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from pages.locators import ProductPageLocators
from utils.logger import logger


class ProductPage(BasePage):
    """Product detail page object."""

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        self.locators = ProductPageLocators()

    def is_product_page_visible(self, timeout: int = 3) -> bool:
        """True if product detail page is visible (Add to bag, Size, etc.)."""
        indicators = [
            self.locators.ADD_TO_BAG,
            self.locators.ADD_TO_BAG_TEXT,
            self.locators.ADD_TO_BAG_DESC,
            self.locators.SIZE_BUTTON,
            self.locators.SELECT_SIZE,
            self.locators.ADD_TO_BAG_TEXT_LOWER,
            self.locators.ADD_TO_BAG_DESC_LOWER,
        ]
        for loc in indicators:
            if self.is_element_present(loc, timeout=timeout):
                return True
        return False

    def is_go_to_bag_or_add_success(self, timeout: int = 3) -> bool:
        """True if Go to bag visible, or size popup gone (DONE clicked)."""
        go_to_bag_locs = [
            self.locators.GO_TO_BAG,
            self.locators.GO_TO_BAG_TEXT,
            self.locators.GO_TO_BAG_TEXT_LOWER,
            self.locators.GO_TO_BAG_DESC_LOWER,
        ]
        for loc in go_to_bag_locs:
            if self.is_element_present(loc, timeout=timeout):
                return True
        try:
            WebDriverWait(self.driver, 1).until(
                EC.invisibility_of_element_located(self.locators.SIZE_POPUP_TITLE)
            )
            return True
        except Exception:
            pass
        return False

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
