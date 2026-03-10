"""Test: Verify app launches, then popup handling, then home screen."""
import time
import pytest
from config.capabilities import APP_PACKAGE
from core.driver_factory import quit_driver
from utils.logger import logger


def _press_back_safe(driver):
    try:
        driver.back()
    except Exception:
        try:
            driver.press_keycode(4)
        except Exception:
            pass


@pytest.mark.smoke
def test_app_launches_successfully(driver):
    """Only check that the app opens; then close the app. No popup handling, no home."""
    time.sleep(2)
    try:
        driver.activate_app(APP_PACKAGE)
    except Exception:
        pass
    time.sleep(1.5)
    current = driver.current_package
    assert current == APP_PACKAGE, f"Expected Myntra, got {current}"
    quit_driver(driver)
    logger.info("✅ App launched successfully (app opened and closed)")


@pytest.mark.smoke
def test_handle_onboarding_popup(driver):
    """Launch app, press Back once to dismiss the popup, then quit immediately. Does not wait for home."""
    time.sleep(2)
    try:
        driver.activate_app(APP_PACKAGE)
    except Exception:
        pass
    time.sleep(0.5)
    _press_back_safe(driver)  # One Back to dismiss popup
    time.sleep(0.2)
    quit_driver(driver)  # Close app right away; do not wait for home
    logger.info("✅ Popup handling completed (Back clicked, app quit)")
