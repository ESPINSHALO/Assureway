"""
Reusable explicit wait utilities for the automation framework.

Purpose: Centralize WebDriverWait-based helpers so page objects avoid duplicated wait logic.
Role: wait_for_element, wait_for_element_clickable, element_exists, safe_click used across pages.
Architecture: Consumed by BasePage and PopupHandler; no dependency on page locators.
"""
from typing import Tuple
from appium.webdriver.webdriver import WebDriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils.logger import logger


def wait_for_element(
    driver: WebDriver,
    locator: Tuple[str, str],
    timeout: int = 15,
) -> "WebElement":
    """Wait for the element to be present in the DOM; return it or raise on timeout."""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
        logger.info(f"Element found: {locator[0]}='{locator[1]}'")
        return element
    except TimeoutException:
        logger.error(f"Timeout waiting for element: {locator}")
        raise


def wait_for_element_clickable(
    driver: WebDriver,
    locator: Tuple[str, str],
    timeout: int = 15,
) -> "WebElement":
    """Wait for the element to be present and clickable; return it or raise on timeout."""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        logger.info(f"Element clickable: {locator[0]}='{locator[1]}'")
        return element
    except TimeoutException:
        logger.error(f"Timeout - element not clickable: {locator}")
        raise


def wait_for_element_visible(
    driver: WebDriver,
    locator: Tuple[str, str],
    timeout: int = 15,
) -> "WebElement":
    """Wait for the element to be visible; return it or raise on timeout."""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
        return element
    except TimeoutException:
        logger.error(f"Timeout - element not visible: {locator}")
        raise


def element_exists(driver: WebDriver, locator: Tuple[str, str], timeout: int = 5) -> bool:
    """Return True if the element is present within the timeout; False otherwise (no raise)."""
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
        return True
    except (TimeoutException, WebDriverException):
        return False


def safe_click(driver: WebDriver, locator: Tuple[str, str], timeout: int = 15) -> bool:
    """Wait for the element to be clickable, then click; return True on success, False on failure."""
    try:
        element = wait_for_element_clickable(driver, locator, timeout)
        element.click()
        logger.info(f"Clicked: {locator[0]}='{locator[1]}'")
        return True
    except Exception as e:
        logger.warning(f"Click failed for {locator}: {e}")
        return False
