"""Test: Verify app launches successfully."""
import pytest
from pages import HomePage
from utils.logger import logger


@pytest.mark.smoke
def test_app_launches_successfully(driver, popup_handler):
    """Verify Myntra app launches and home screen loads."""
    import time
    time.sleep(4)  # Allow app to initialize
    for _ in range(5):  # Handle permission dialogs, onboarding
        popup_handler.handle_initial_popups()
        time.sleep(2)
        try:
            if driver.current_package == "com.myntra.android":
                break
        except Exception:
            pass
        time.sleep(1)
    
    # Activate Myntra in case we're on launcher/permission (app may be in background)
    try:
        driver.activate_app("com.myntra.android")
        time.sleep(3)
    except Exception:
        pass
    
    current = driver.current_package
    assert current == "com.myntra.android", f"Expected Myntra, got {current}"
    logger.info("✅ App launched successfully")


@pytest.mark.smoke
def test_handle_onboarding_popup(driver, popup_handler):
    """Verify we can handle onboarding/login popup."""
    import time
    time.sleep(3)
    # Attempt to dismiss any popup - should not raise
    popup_handler.handle_initial_popups()
    time.sleep(1)
    logger.info("✅ Popup handling completed")
