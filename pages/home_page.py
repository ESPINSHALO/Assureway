"""Home page interactions for Myntra app."""
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from pages.locators import HomePageLocators
from utils.logger import logger


class HomePage(BasePage):
    """Home screen page object."""

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        self.locators = HomePageLocators()

    def tap_search(self) -> bool:
        """Tap the search bar quickly: short timeouts, multiple locators, click or tap at center."""
        logger.info("Tapping search icon")
        # Same locators as script perform_search; short timeout so we don't stay long on home
        search_locators = [
            (AppiumBy.ID, "com.myntra.android:id/search_widget_text"),
            self.locators.SEARCH_CONTAINER,
            self.locators.SEARCH_ICON,
            (AppiumBy.XPATH, "//*[contains(@text,'Jeans') or contains(@text,'Search') or contains(@content-desc,'Search')]"),
            (AppiumBy.ACCESSIBILITY_ID, "Search"),
        ]
        wait = WebDriverWait(self.driver, 0.7)
        for loc in search_locators:
            try:
                el = wait.until(EC.visibility_of_element_located(loc))
                if not el or not el.is_displayed():
                    continue
                try:
                    el.click()
                    logger.info("Search bar clicked")
                    return True
                except Exception:
                    pass
                try:
                    loc_ = el.location
                    sz = el.size
                    cx = loc_["x"] + sz["width"] // 2
                    cy = loc_["y"] + sz["height"] // 2
                    self.driver.tap([(cx, cy)])
                    logger.info("Search bar tapped at center")
                    return True
                except Exception:
                    pass
            except Exception:
                continue
        return self.tap(self.locators.SEARCH_ICON)

    def tap_bag(self) -> bool:
        """Tap the bag icon to open shopping bag."""
        logger.info("Tapping bag icon")
        return self.tap(self.locators.BAG_ICON)

    def is_home_loaded(self, timeout: int = 8) -> bool:
        """Verify home screen is loaded (search bar or Home tab visible)."""
        for loc in [
            self.locators.SEARCH_ICON,
            self.locators.SEARCH_CONTAINER,
            self.locators.HOME_TAB,
            self.locators.HOME_TAB_ALT,
        ]:
            if self.is_element_present(loc, timeout=timeout):
                return True
        return False
