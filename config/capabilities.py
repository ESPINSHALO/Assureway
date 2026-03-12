"""
Appium capabilities configuration for the Myntra Android app.

Purpose: Centralizes all desired capabilities and app constants used by the driver.
Role: Single source of truth for platform, app package, activity, and device settings.
Architecture: Consumed by core.driver_factory when creating the Appium session.
"""
import os

from appium.options.android import UiAutomator2Options

APP_PACKAGE = os.getenv("APP_PACKAGE", "com.myntra.android")
APP_ACTIVITY = os.getenv(
    "APP_ACTIVITY",
    "com.myntra.android.activities.react.ReactActivity.MBB_PRIMARY",
)
DEVICE_NAME = os.getenv("DEVICE_NAME", "Android Emulator")
PLATFORM_NAME = os.getenv("PLATFORM_NAME", "Android")


def get_android_capabilities() -> UiAutomator2Options:
    """
    Build and return UiAutomator2 options for the Myntra Android app.

    Used by the driver factory to establish the Appium session. Prerequisites:
    Android emulator running, Myntra installed, Appium server started (appium).
    """
    options = UiAutomator2Options()
    options.platform_name = PLATFORM_NAME
    options.automation_name = "UiAutomator2"
    options.app_package = APP_PACKAGE
    options.app_activity = APP_ACTIVITY
    options.device_name = DEVICE_NAME
    options.udid = os.getenv("UDID", "")
    options.auto_grant_permissions = True
    options.uiautomator2_server_launch_timeout = int(os.getenv("U2_LAUNCH_TIMEOUT", "60000"))
    options.no_reset = False
    options.full_reset = False
    return options
