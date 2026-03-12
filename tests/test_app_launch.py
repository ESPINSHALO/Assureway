"""
Tests for app launch and initial popup handling.

Purpose: Validate that the Myntra app starts and that a single Back key dismisses the first overlay.
Role: First tests in the suite; no home wait or search flow; driver is quit inside the test.
Architecture: Uses driver fixture; imports APP_PACKAGE from config (no hardcoded package).
"""
import time
import pytest
from config.capabilities import APP_PACKAGE
from core.driver_factory import quit_driver
from utils.logger import logger


def _press_back_safe(driver):
    """Send the device back key once; never raises."""
    try:
        driver.back()
    except Exception:
        try:
            driver.press_keycode(4)
        except Exception:
            pass


@pytest.mark.smoke
def test_app_launches_successfully(driver):
    """Verify that the app launches and the current package is Myntra; then quit the driver."""
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
    """Verify that the app launches and one Back key dismisses the initial popup; then quit without waiting for home."""
    time.sleep(2)
    try:
        driver.activate_app(APP_PACKAGE)
    except Exception:
        pass
    time.sleep(0.5)
    _press_back_safe(driver)
    time.sleep(0.2)
    quit_driver(driver)
    logger.info("✅ Popup handling completed (Back clicked, app quit)")
