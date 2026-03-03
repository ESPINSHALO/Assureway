"""
Pytest configuration and fixtures for Myntra automation.
"""
import pytest
from appium.webdriver.webdriver import WebDriver
from core.driver_factory import create_driver, quit_driver
from pages import HomePage, SearchPage, ProductPage, BagPage, PopupHandler
from utils.logger import logger


@pytest.fixture(scope="function")
def driver() -> WebDriver:
    """
    Create Appium driver for each test.
    Ensures fresh app state per test.
    """
    drv = create_driver()
    yield drv
    quit_driver(drv)


@pytest.fixture(scope="function")
def home_page(driver: WebDriver) -> HomePage:
    """Home page object with driver."""
    return HomePage(driver)


@pytest.fixture(scope="function")
def search_page(driver: WebDriver) -> SearchPage:
    """Search page object."""
    return SearchPage(driver)


@pytest.fixture(scope="function")
def product_page(driver: WebDriver) -> ProductPage:
    """Product page object."""
    return ProductPage(driver)


@pytest.fixture(scope="function")
def bag_page(driver: WebDriver) -> BagPage:
    """Bag page object."""
    return BagPage(driver)


@pytest.fixture(scope="function")
def popup_handler(driver: WebDriver) -> PopupHandler:
    """Popup handler."""
    return PopupHandler(driver)


@pytest.fixture(scope="function")
def app_launched(driver: WebDriver, popup_handler: PopupHandler):
    """
    Fixture that launches app and handles initial popups.
    Use when test needs app to be ready on home screen.
    """
    import time
    time.sleep(3)  # Wait for app to fully load
    popup_handler.handle_initial_popups()
    time.sleep(1)
    return driver
