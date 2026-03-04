"""Appium driver factory for Android."""
from appium import webdriver
from appium.webdriver.webdriver import WebDriver
from config.capabilities import get_android_capabilities
from utils.logger import logger


APPIUM_SERVER_URL = "http://127.0.0.1:4723"
# Use 0 so WebDriverWait timeouts control timing; avoids 10s block per failed find
DEFAULT_IMPLICIT_WAIT = 0


def create_driver(
    server_url: str = APPIUM_SERVER_URL,
    implicit_wait: int = DEFAULT_IMPLICIT_WAIT,
) -> WebDriver:
    """
    Create and return an Appium WebDriver instance for Myntra Android app.
    
    Prerequisites:
    - Appium server running (appium)
    - Android emulator running with Myntra installed
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
    """Safely quit the driver."""
    if driver:
        try:
            driver.quit()
            logger.info("Driver closed successfully")
        except Exception as e:
            logger.warning(f"Error closing driver: {e}")
