"""Home page interactions for Myntra app."""
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
        """
        Tap the search bar with strict, locator-only targeting.
        Uses only the search widget resource-id / accessibility-id.
        Does not tap any coordinates unless they belong to a located element.
        """
        logger.info("Tapping search icon")

        # Only use stable, specific locators for the search bar (no broad XPaths).
        search_locators = [
            self.locators.SEARCH_CONTAINER,
            self.locators.SEARCH_ICON,
            self.locators.SEARCH_BAR_PLACEHOLDER,
            self.locators.SEARCH_ACCESSIBILITY_ID,
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
                    try:
                        # Use a precise tap at the element center as a fallback, based on element bounds.
                        loc_ = el.location
                        sz = el.size
                        cx = loc_["x"] + sz["width"] // 2
                        cy = loc_["y"] + sz["height"] // 2
                        self.driver.execute_script(
                            "mobile: clickGesture", {"x": int(cx), "y": int(cy)}
                        )
                        logger.info("Search bar tapped at center")
                        return True
                    except Exception:
                        continue
            except Exception:
                continue

        # Do not guess coordinates outside a located element – fail fast instead of mis-tapping.
        logger.warning("Search bar element not found by id/accessibility; tap_search returning False")
        return False

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
