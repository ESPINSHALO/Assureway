"""Home page interactions for Myntra app."""
from appium.webdriver.webdriver import WebDriver
from pages.base_page import BasePage
from pages.locators import HomePageLocators
from utils.logger import logger


class HomePage(BasePage):
    """Home screen page object."""

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        self.locators = HomePageLocators()

    def tap_search(self) -> bool:
        """Tap the search icon."""
        logger.info("Tapping search icon")
        return self.tap(self.locators.SEARCH_ICON)

    def tap_bag(self) -> bool:
        """Tap the bag icon to open shopping bag."""
        logger.info("Tapping bag icon")
        return self.tap(self.locators.BAG_ICON)

    def is_home_loaded(self) -> bool:
        """Verify home screen is loaded."""
        return self.is_element_present(self.locators.SEARCH_ICON)
