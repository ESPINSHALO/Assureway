"""
Base page class for the Page Object Model.

Purpose: Shared behavior and helpers for all screen-specific page objects.
Role: Centralizes tap, find, scroll, and back actions used across Home, Search, Product, Bag, Popup.
Architecture: All page classes in this package inherit from BasePage.
"""
from typing import Tuple
from appium.webdriver.webdriver import WebDriver
from appium.webdriver.common.appiumby import AppiumBy
from utils.waits import wait_for_element, wait_for_element_clickable, safe_click, element_exists
from utils.logger import logger


class BasePage:
    """
    Base class for all Myntra page objects.

    Provides common actions (tap, find, scroll, back) and coordinate-based fallbacks
    for screens where locators are unreliable (e.g. profile back, onboarding close).
    """

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

    def tap(self, locator: Tuple[str, str], timeout: int = 15) -> bool:
        """Perform a click on the element identified by the given locator."""
        return safe_click(self.driver, locator, timeout)

    def find_element(self, locator: Tuple[str, str], timeout: int = 15):
        """Wait for and return the first matching element."""
        return wait_for_element(self.driver, locator, timeout)

    def is_element_present(self, locator: Tuple[str, str], timeout: int = 5) -> bool:
        """Return True if the element is present within the given timeout."""
        return element_exists(self.driver, locator, timeout)

    def scroll_down(self, duration_ms: int = 500) -> None:
        """Scroll the screen downward to reveal content below the fold."""
        size = self.driver.get_window_size()
        start_x = size["width"] // 2
        start_y = int(size["height"] * 0.8)
        end_y = int(size["height"] * 0.2)
        self.driver.swipe(start_x, start_y, start_x, end_y, duration_ms)
        logger.debug("Scrolled down")

    def scroll_up(self, duration_ms: int = 500) -> None:
        """Scroll the screen upward."""
        size = self.driver.get_window_size()
        start_x = size["width"] // 2
        start_y = int(size["height"] * 0.2)
        end_y = int(size["height"] * 0.8)
        self.driver.swipe(start_x, start_y, start_x, end_y, duration_ms)
        logger.debug("Scrolled up")

    def go_back(self) -> None:
        """Send the device back key to navigate back or dismiss overlays."""
        self.driver.back()
        logger.info("Pressed back button")

    def tap_coordinates(self, x: int, y: int) -> None:
        """Tap at (x, y); used when elements lack stable resource-id or content-desc."""
        self.driver.tap([(x, y)])
        logger.debug(f"Tapped at ({x}, {y})")

    def tap_top_left_back(self) -> bool:
        """
        Tap the top-left back arrow on the Profile screen to return to home.

        Uses a fixed offset below the status bar to support different resolutions.
        """
        try:
            size = self.driver.get_window_size()
            w, h = size["width"], size["height"]
            x, y = 45, int(h * 0.08)
            self.tap_coordinates(x, y)
            return True
        except Exception as e:
            logger.warning(f"Tap top-left back failed: {e}")
            return False

    def tap_top_right_close(self) -> bool:
        """
        Tap the top-right area to dismiss onboarding or overlay close (X) when no locator exists.
        """
        try:
            size = self.driver.get_window_size()
            w, h = size["width"], size["height"]
            x, y = int(w * 0.92), int(h * 0.08)
            self.tap_coordinates(x, y)
            return True
        except Exception as e:
            logger.warning(f"Tap top-right failed: {e}")
            return False
