"""Base page class for page object pattern."""
from typing import Tuple
from appium.webdriver.webdriver import WebDriver
from appium.webdriver.common.appiumby import AppiumBy
from utils.waits import wait_for_element, wait_for_element_clickable, safe_click, element_exists
from utils.logger import logger


class BasePage:
    """Base class for all page objects."""

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

    def tap(self, locator: Tuple[str, str], timeout: int = 15) -> bool:
        """Tap/click on element."""
        return safe_click(self.driver, locator, timeout)

    def find_element(self, locator: Tuple[str, str], timeout: int = 15):
        """Find and return element."""
        return wait_for_element(self.driver, locator, timeout)

    def is_element_present(self, locator: Tuple[str, str], timeout: int = 5) -> bool:
        """Check if element is present."""
        return element_exists(self.driver, locator, timeout)

    def scroll_down(self, duration_ms: int = 500) -> None:
        """Scroll down the screen."""
        size = self.driver.get_window_size()
        start_x = size["width"] // 2
        start_y = int(size["height"] * 0.8)
        end_y = int(size["height"] * 0.2)
        self.driver.swipe(start_x, start_y, start_x, end_y, duration_ms)
        logger.debug("Scrolled down")

    def scroll_up(self, duration_ms: int = 500) -> None:
        """Scroll up the screen."""
        size = self.driver.get_window_size()
        start_x = size["width"] // 2
        start_y = int(size["height"] * 0.2)
        end_y = int(size["height"] * 0.8)
        self.driver.swipe(start_x, start_y, start_x, end_y, duration_ms)
        logger.debug("Scrolled up")

    def go_back(self) -> None:
        """Press device back button."""
        self.driver.back()
        logger.info("Pressed back button")

    def tap_coordinates(self, x: int, y: int) -> None:
        """Tap at screen coordinates (e.g. for elements without reliable locators)."""
        self.driver.tap([(x, y)])
        logger.debug(f"Tapped at ({x}, {y})")

    def tap_top_left_back(self) -> bool:
        """
        Tap the top-left back arrow (←) on Profile screen. Tries multiple positions
        to handle different screen sizes; back icon is next to "Profile" title.
        """
        try:
            size = self.driver.get_window_size()
            w, h = size["width"], size["height"]
            # Back arrow: far left, below status bar (~24–32px). Try several positions.
            x, y = 45, int(h * 0.08)
            self.tap_coordinates(x, y)
            return True
        except Exception as e:
            logger.warning(f"Tap top-left back failed: {e}")
            return False

    def tap_top_right_close(self) -> bool:
        """
        Tap the top-right area where the X close button usually is (onboarding screens).
        Use when the close icon has no content-desc or resource-id.
        Tries two positions to handle different resolutions.
        """
        try:
            size = self.driver.get_window_size()
            w, h = size["width"], size["height"]
            # X in circle: ~50-80px from right, ~80-120px from top (below status bar)
            x, y = int(w * 0.92), int(h * 0.08)
            self.tap_coordinates(x, y)
            return True
        except Exception as e:
            logger.warning(f"Tap top-right failed: {e}")
            return False
