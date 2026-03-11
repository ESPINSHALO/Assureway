"""Home page interactions for Myntra app."""
import time

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
        # Include both ID and tight XPath for the rounded search container.
        search_locators = [
            self.locators.SEARCH_CONTAINER,
            self.locators.SEARCH_CONTAINER_XPATH,
            self.locators.SEARCH_ICON,
            self.locators.SEARCH_BAR_PLACEHOLDER,
            self.locators.SEARCH_ACCESSIBILITY_ID,
        ]

        # The search bar lives near the top of the screen; never tap anything outside this band.
        try:
            size = self.driver.get_window_size()
            h = size["height"]
        except Exception:
            h = 2400
        min_y = int(h * 0.08)
        max_y = int(h * 0.42)

        # Wait for search bar to be visible (home can load slowly after app_launched).
        for loc in search_locators:
            try:
                WebDriverWait(self.driver, 4).until(EC.visibility_of_element_located(loc))
                break
            except Exception:
                continue

        # Poll for tap: longer window so we don't miss when UI is slow.
        deadline = time.time() + 4.0
        poll = 0.25
        while time.time() < deadline:
            for loc in search_locators:
                try:
                    els = self.driver.find_elements(*loc)
                except Exception:
                    continue
                for el in els:
                    try:
                        if not el.is_displayed():
                            continue
                        loc_ = el.location
                        sz = el.size
                        cy = loc_["y"] + sz["height"] // 2
                        # Ignore any element whose vertical position is not in the search-bar band.
                        if cy < min_y or cy > max_y:
                            continue
                        try:
                            el.click()
                            logger.info("Search bar clicked")
                            return True
                        except Exception:
                            try:
                                cx = loc_["x"] + sz["width"] // 2
                                self.driver.execute_script(
                                    "mobile: clickGesture",
                                    {"x": int(cx), "y": int(cy)},
                                )
                                logger.info("Search bar tapped at center")
                                return True
                            except Exception:
                                continue
                    except Exception:
                        continue
            time.sleep(poll)

        # Do not guess coordinates outside a located element – fail fast instead of mis-tapping.
        logger.warning("Search bar element not found by id/accessibility; tap_search returning False")
        return False

    def tap_bag(self, timeout: int = 5) -> bool:
        """
        Tap the bag icon to open shopping bag.
        Waits for home to be ready, tries multiple locators, then bottom-right fallback
        so cart opens reliably after returning from login.
        """
        logger.info("Tapping bag icon")
        # Wait for home/bottom nav so bag icon is available
        try:
            WebDriverWait(self.driver, min(2, timeout)).until(
                EC.visibility_of_element_located(self.locators.HOME_TAB)
            )
        except Exception:
            pass
        time.sleep(0.3)
        bag_locators = [
            self.locators.BAG_ICON,
            self.locators.BAG_ICON_ACCESSIBILITY,
            self.locators.BAG_ICON_XPATH,
        ]
        for loc in bag_locators:
            try:
                el = WebDriverWait(self.driver, 2).until(
                    EC.element_to_be_clickable(loc)
                )
                if el and el.is_displayed():
                    el.click()
                    logger.info("Bag icon clicked")
                    return True
            except Exception:
                continue
        # Fallback: bottom-right tap (same as script when locators fail after return from login)
        try:
            time.sleep(0.2)
            sz = self.driver.get_window_size()
            w, h = sz["width"], sz["height"]
            x, y = int(w * 0.92), int(h * 0.96)
            self.driver.execute_script("mobile: clickGesture", {"x": x, "y": y})
            logger.info("Bag icon tapped (bottom-right fallback)")
            return True
        except Exception as e:
            logger.warning("Bag tap fallback failed: %s", e)
        return False

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

    def wait_until_home_visible(self, timeout: int = 10) -> bool:
        """Wait until home screen is visible. Tries search bar and Home tab locators."""
        locs = [
            self.locators.SEARCH_CONTAINER,
            self.locators.SEARCH_CONTAINER_XPATH,
            self.locators.SEARCH_BAR_PLACEHOLDER,
            self.locators.HOME_TAB,
            self.locators.HOME_TAB_ALT,
        ]
        per_loc = max(1, timeout // len(locs))
        for loc in locs:
            try:
                WebDriverWait(self.driver, per_loc).until(
                    EC.visibility_of_element_located(loc)
                )
                return True
            except Exception:
                continue
        return False
