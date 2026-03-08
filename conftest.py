"""
Pytest configuration and fixtures for Myntra automation.

Test order (by design): app launch → popups → home → tap search → search page → ...
Each test gets a fresh app session (driver per test). This keeps tests independent.
For one continuous flow without restarts, run: pytest tests/test_full_e2e_flow.py -v

On test failure, a screenshot is saved to reports/screenshots/.
"""
import os
import re
import sys
import time
from datetime import datetime

import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from appium.webdriver.webdriver import WebDriver
from core.driver_factory import create_driver, quit_driver
from pages import HomePage, SearchPage, ProductPage, BagPage, PopupHandler
from pages.locators import HomePageLocators
from utils.logger import logger

# Folder for failure screenshots (inside reports so all test artifacts are in one place)
SCREENSHOTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports", "screenshots")

# Run order: launch → home → search flow → cart/checkout → full E2E (navigation/add_to_bag/bag_ops removed as redundant)
TEST_FILE_ORDER = [
    "test_app_launch.py",       # 1. App launches, popups handled
    "test_home_screen.py",      # 2. Reach home, tap search icon
    "test_search_flow.py",      # 3. Search → Gender → Sort → open product → select size & add to bag
    "test_cart_checkout_flow.py",  # 4. Navigate home → open cart → qty 2 → Place Order → back from login → remove → empty → home
    "test_full_e2e_flow.py",    # 5. Full flow end-to-end
]

# Order of tests *within* each file (so flow is correct; pytest would sort by name otherwise)
TEST_ORDER_IN_FILE = {
    "test_search_flow.py": [
        "test_search_for_product",       # 1. Search first
        "test_gender_select_male",       # 2. Gender → Male
        "test_sort_select_discounts",   # 3. Sort → Discounts
        "test_open_first_product",      # 4. Open first product
        "test_select_size_and_add_to_bag",  # 5. Select size, Add to bag, confirm
    ],
    "test_app_launch.py": [
        "test_app_launches_successfully",
        "test_handle_onboarding_popup",
    ],
    "test_home_screen.py": [
        "test_home_screen_loads",
        "test_tap_search_icon",
    ],
    "test_cart_checkout_flow.py": [
        "test_navigate_to_home_after_add_to_bag",
        "test_open_cart_increase_quantity_done",
        "test_click_place_order_opens_login",
        "test_back_from_login_to_home",
        "test_remove_product_from_cart",
        "test_verify_empty_cart_and_return_home",
    ],
}


def pytest_collection_modifyitems(session, config, items):
    """Reorder tests: by file (TEST_FILE_ORDER), then by explicit order within file (TEST_ORDER_IN_FILE)."""
    file_order_map = {name: i for i, name in enumerate(TEST_FILE_ORDER)}

    def key(item):
        path = item.nodeid.split("::")[0]
        filename = path.split("/")[-1] if "/" in path else path
        file_order = file_order_map.get(filename, 999)
        test_name = item.nodeid.split("::")[-1] if "::" in item.nodeid else item.nodeid
        in_file_order = TEST_ORDER_IN_FILE.get(filename)
        if in_file_order and test_name in in_file_order:
            test_index = in_file_order.index(test_name)
            return (file_order, test_index, item.nodeid)
        return (file_order, 999, item.nodeid)

    items.sort(key=key)


def _get_driver_from_item(item):
    """Get WebDriver from test item (driver or app_launched fixture). Returns None if not found."""
    driver = None
    # 1) Request fixture values (cached; does not re-run fixtures)
    request = getattr(item, "_request", None)
    if request is not None:
        for fixture_name in ("app_launched", "driver"):
            try:
                val = request.getfixturevalue(fixture_name)
                if val is not None and isinstance(val, WebDriver):
                    return val
            except Exception:
                continue
    # 2) Fallback: scan funcargs for a WebDriver instance
    funcargs = getattr(item, "funcargs", None)
    if isinstance(funcargs, dict):
        for val in funcargs.values():
            if isinstance(val, WebDriver):
                return val
    return None


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """On test failure, save a screenshot to reports/screenshots/ (for all tests that use driver or app_launched)."""
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or report.passed:
        return
    driver = _get_driver_from_item(item)
    if driver is None:
        logger.warning("No WebDriver found for failed test %s - screenshot skipped", item.name)
        return
    try:
        os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
        safe_name = re.sub(r"[^\w\-.]", "_", item.name)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{safe_name}_{timestamp}.png"
        filepath = os.path.join(SCREENSHOTS_DIR, filename)
        filepath = os.path.abspath(filepath)
        driver.save_screenshot(filepath)
        logger.info("Screenshot saved on failure: %s", filepath)
        sys.stderr.write(f"[pytest] Screenshot saved: {filepath}\n")
    except Exception as e:
        logger.warning("Could not save failure screenshot: %s", e)
        sys.stderr.write(f"[pytest] Screenshot failed: {e}\n")


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


MYNTRA_PACKAGE = "com.myntra.android"


def _press_back_safe(driver):
    """Press Back once. Never raises — use for startup popup handling."""
    try:
        driver.back()
    except Exception:
        try:
            driver.press_keycode(4)
        except Exception:
            pass


def _wait_for_home(driver, timeout_per_loc: int = 2):
    """Wait until home screen is visible (search bar or Home tab). Returns True if found."""
    locators = [
        HomePageLocators.SEARCH_CONTAINER,
        HomePageLocators.SEARCH_CONTAINER_XPATH,
        HomePageLocators.SEARCH_BAR_PLACEHOLDER,
        HomePageLocators.HOME_TAB,
        HomePageLocators.HOME_TAB_ALT,
    ]
    for loc in locators:
        try:
            WebDriverWait(driver, timeout_per_loc).until(EC.visibility_of_element_located(loc))
            return True
        except Exception:
            continue
    return False


@pytest.fixture(scope="function")
def app_launched(driver: WebDriver, popup_handler: PopupHandler):
    """
    Fixture that launches app, handles initial popups, and waits for home screen.
    Use when test needs app to be ready on home screen (search bar visible).
    Startup: activate app → wait for first screen → Back once (safe) → popups → wait for home.
    """
    time.sleep(2.5)
    try:
        driver.activate_app(MYNTRA_PACKAGE)
    except Exception:
        pass
    time.sleep(0.5)
    _press_back_safe(driver)
    time.sleep(0.5)
    try:
        popup_handler.handle_initial_popups()
    except Exception:
        pass
    time.sleep(0.5)
    if not _wait_for_home(driver, timeout_per_loc=3):
        _press_back_safe(driver)
        time.sleep(0.5)
        try:
            popup_handler.dismiss_popup()
            time.sleep(0.5)
        except Exception:
            pass
        _wait_for_home(driver, timeout_per_loc=2)
    return driver
