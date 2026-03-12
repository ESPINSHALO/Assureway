"""
Appium driver factory for the Myntra Android automation framework.

Purpose: Creates and tears down the Appium WebDriver session.
Role: Reusable driver lifecycle management; used by pytest fixtures and standalone scripts.
Architecture: Depends on config.capabilities for options; used by conftest and scripts.
"""
from appium import webdriver
from appium.webdriver.webdriver import WebDriver
from config.capabilities import get_android_capabilities
from utils.logger import logger


APPIUM_SERVER_URL = "http://127.0.0.1:4723"
DEFAULT_IMPLICIT_WAIT = 0


def create_driver(
    server_url: str = APPIUM_SERVER_URL,
    implicit_wait: int = DEFAULT_IMPLICIT_WAIT,
) -> WebDriver:
    """
    Create and return an Appium WebDriver instance for the Myntra app.

    Prerequisites: Appium server running, Android emulator with Myntra installed.
    """
    options = get_android_capabilities()
    
    logger.info("Connecting to Appium server and launching Myntra app...")
    driver = webdriver.Remote(
        command_executor=server_url,
        options=options,
    )
    driver.implicitly_wait(implicit_wait)
    logger.info("Driver created successfully")
    
    return driver


def quit_driver(driver: WebDriver) -> None:
    """Close the driver session; logs and swallows errors to avoid masking test failures."""
    if driver:
        try:
            driver.quit()
            logger.info("Driver closed successfully")
        except Exception as e:
            logger.warning(f"Error closing driver: {e}")
