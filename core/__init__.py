"""Core automation components."""
from core.driver_factory import create_driver, quit_driver, APPIUM_SERVER_URL

__all__ = ["create_driver", "quit_driver", "APPIUM_SERVER_URL"]
