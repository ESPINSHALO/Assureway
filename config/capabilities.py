"""
Appium capabilities configuration for Myntra Android app.
Update these values to match your Android emulator and Myntra app.
"""
from appium.options.android import UiAutomator2Options


def get_android_capabilities() -> UiAutomator2Options:
    """
    Returns Android UiAutomator2 capabilities for Myntra app.
    
    Prerequisites:
    1. Start Android emulator from Android Studio
    2. Install Myntra APK on emulator (download from Play Store or APKMirror)
    3. Start Appium server: appium
    """
    options = UiAutomator2Options()
    
    # Platform
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    
    # App - Use app_package + app_activity for already installed app
    # Find package/activity via: adb shell dumpsys window | grep -E 'mCurrentFocus'
    options.app_package = "com.myntra.android"
    # Use MBB_PRIMARY - default launcher activity (from: adb shell cmd package resolve-activity)
    options.app_activity = "com.myntra.android.activities.react.ReactActivity.MBB_PRIMARY"
    
    # Alternative: Use APK path if app needs to be installed
    # options.app = "/path/to/myntra.apk"
    
    # Emulator/Device settings
    options.device_name = "Android Emulator"
    options.udid = ""  # Leave empty for default emulator, or use: adb devices
    
    # Auto-grant runtime permissions (location, notifications, etc.) to skip permission dialogs
    options.auto_grant_permissions = True
    
    # Optional: Disable animations for faster execution
    options.no_reset = False  # Set True to preserve app state between runs
    options.full_reset = False
    
    return options
