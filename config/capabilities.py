"""
Appium capabilities configuration for Myntra Android app.
Application constants are defined once here and can be overridden via environment variables.
"""
import os

from appium.options.android import UiAutomator2Options

# Application constants - override via env for different environments
APP_PACKAGE = os.getenv("APP_PACKAGE", "com.myntra.android")
# Launcher activity. Get from device: adb shell cmd package resolve-activity -c android.intent.category.LAUNCHER com.myntra.android
APP_ACTIVITY = os.getenv(
    "APP_ACTIVITY",
    "com.myntra.android.activities.react.ReactActivity.MBB_PRIMARY",
)
DEVICE_NAME = os.getenv("DEVICE_NAME", "Android Emulator")
PLATFORM_NAME = os.getenv("PLATFORM_NAME", "Android")


def get_android_capabilities() -> UiAutomator2Options:
    """
    Returns Android UiAutomator2 capabilities for Myntra app.
    Uses centralized APP_PACKAGE, APP_ACTIVITY, DEVICE_NAME, PLATFORM_NAME.

    Prerequisites:
    1. Start Android emulator from Android Studio
    2. Install Myntra APK on emulator (download from Play Store or APKMirror)
    3. Start Appium server: appium
    """
    options = UiAutomator2Options()

    # Platform
    options.platform_name = PLATFORM_NAME
    options.automation_name = "UiAutomator2"

    # App - Use app_package + app_activity for already installed app
    # Find package/activity via: adb shell dumpsys window | grep -E 'mCurrentFocus'
    options.app_package = APP_PACKAGE
    options.app_activity = APP_ACTIVITY

    # Alternative: Use APK path if app needs to be installed
    # options.app = "/path/to/myntra.apk"

    # Emulator/Device settings
    options.device_name = DEVICE_NAME
    options.udid = os.getenv("UDID", "")  # Leave empty for default emulator, or use: adb devices
    
    # Auto-grant runtime permissions (location, notifications, etc.) to skip permission dialogs
    options.auto_grant_permissions = True

    # Give UiAutomator2 server more time to start (helps when instrumentation is slow or blocked)
    options.uiautomator2_server_launch_timeout = int(os.getenv("U2_LAUNCH_TIMEOUT", "60000"))
    
    # Optional: Disable animations for faster execution
    options.no_reset = False  # Set True to preserve app state between runs
    options.full_reset = False
    
    return options
