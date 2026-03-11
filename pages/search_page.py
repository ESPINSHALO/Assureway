"""Search page interactions for Myntra app."""
import time

from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from pages.locators import SearchPageLocators, HomePageLocators
from utils.logger import logger


class SearchPage(BasePage):
    """Search screen page object."""

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        self.locators = SearchPageLocators()
        self.home_locators = HomePageLocators()

    def search_from_home(self, search_text: str, timeout: int = 15) -> bool:
        """
        Search from Myntra home using Appium locators and WebDriverWait.
        1. Wait for home stable (bottom nav Home tab).
        2. Click search container.
        3. Wait for EditText, click it, clear, type, press Enter.
        4. Wait for search results container.
        """
        try:
            logger.info("Step 1: Waiting for home screen stable (Home tab)...")
            WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(HomePageLocators.HOME_TAB)
            )
            logger.info("Home tab visible – home screen stable.")
        except Exception:
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable(HomePageLocators.HOME_TAB_ALT)
                )
                logger.info("Home tab (alt) visible – home screen stable.")
            except Exception as e:
                logger.warning(f"Home tab wait: {e}")

        try:
            logger.info("Step 2: Locating search container (rounded search bar)...")
            search_container = None
            for loc in [HomePageLocators.SEARCH_CONTAINER, HomePageLocators.SEARCH_CONTAINER_XPATH]:
                try:
                    search_container = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable(loc)
                    )
                    logger.info(f"Search container found: {loc[0]}")
                    break
                except Exception:
                    continue
            if not search_container:
                raise Exception("Search container not found")

            logger.info("Step 3: Clicking search container...")
            search_container.click()
            time.sleep(1.5)

            logger.info("Step 4: Waiting for search input EditText...")
            search_input = None
            for loc in [
                self.locators.SEARCH_INPUT,
                self.locators.SEARCH_INPUT_EDIT,
                self.locators.SEARCH_INPUT_PLACEHOLDER_JEANS,
                self.locators.SEARCH_INPUT_EDIT_XPATH,
            ]:
                try:
                    search_input = WebDriverWait(self.driver, 8).until(
                        EC.presence_of_element_located(loc)
                    )
                    logger.info(f"Search input found: {loc[0]}")
                    break
                except Exception:
                    continue
            if not search_input:
                raise Exception("Search input EditText not found")

            logger.info("Step 5: Clicking EditText explicitly...")
            search_input.click()
            time.sleep(0.5)

            logger.info("Step 6: Clearing existing text...")
            search_input.clear()
            time.sleep(0.3)

            logger.info("Step 7: Typing search term via send_keys...")
            search_input.send_keys(search_text)
            time.sleep(0.5)

            logger.info("Step 8: Pressing Enter (keycode 66)...")
            self.driver.press_keycode(66)
            time.sleep(1)

            logger.info("Step 9: Waiting for search results container...")
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(self.locators.SEARCH_RESULTS_LIST)
                )
                logger.info("Search results container visible.")
            except Exception:
                try:
                    WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located(self.locators.SEARCH_RESULTS_XPATH)
                    )
                    logger.info("Search results (XPath) visible.")
                except Exception as e:
                    logger.warning(f"Results container wait: {e}")

            logger.info(f"Search completed for: {search_text}")
            return True
        except Exception as e:
            logger.error(f"Search from home failed: {e}")
            return False

    def enter_search_term(self, search_text: str) -> bool:
        """Enter search query. Many apps auto-search as you type."""
        try:
            element = self.find_element(self.locators.SEARCH_INPUT)
            element.clear()
            element.send_keys(search_text)
            self.driver.press_keycode(66)
            logger.info(f"Searched for: {search_text}")
            return True
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return False

    def tap_first_result(self) -> bool:
        """Tap the first product in search results."""
        logger.info("Tapping first search result")
        return self.tap(self.locators.FIRST_PRODUCT)

    def has_results(self) -> bool:
        """Check if search returned results."""
        return self.is_element_present(self.locators.FIRST_PRODUCT, timeout=10)

    def is_listing_visible(self, timeout: int = 5) -> bool:
        """True if listing page is shown (SORT or GENDER button visible)."""
        return (
            self.is_element_present(self.locators.SORT_BUTTON, timeout=timeout)
            or self.is_element_present(self.locators.GENDER_BUTTON, timeout=timeout)
        )

    def is_listing_gone(self, timeout: int = 1) -> bool:
        """True if listing left (SORT or GENDER no longer visible)."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(self.locators.SORT_BUTTON)
            )
            return True
        except Exception:
            pass
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(self.locators.GENDER_BUTTON)
            )
            return True
        except Exception:
            pass
        return False
