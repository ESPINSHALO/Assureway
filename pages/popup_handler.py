"""
Page Object for dismissible popups and overlays (onboarding, login, profile).

Purpose: Dismiss onboarding, permission, profile, and login screens so tests reach home or cart.
Role: Used by app_launched fixture and tests that need to close login after Place Order.
Architecture: Inherits BasePage; uses PopupLocators and HomePageLocators for detection.
"""
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config.capabilities import APP_PACKAGE
from pages.base_page import BasePage
from pages.home_page import HomePage
from pages.locators import PopupLocators, HomePageLocators
from utils.logger import logger
from utils.waits import element_exists, safe_click


class PopupHandler(BasePage):
    """
    Dismissible overlays: profile back, onboarding close, permissions, login screen detection.

    Provides dismiss_popup (single attempt), handle_initial_popups (repeated on launch),
    and is_login_screen_visible for post–Place Order checks.
    """

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        self.locators = PopupLocators()

    def dismiss_popup(self) -> bool:
        """
        Dismiss one overlay: profile (Back), then onboarding (top-right X or close locators).
        Returns True if something was dismissed; avoids tapping when already on home.
        """
        try:
            if self.driver.current_package == APP_PACKAGE:
                on_profile = (
                    element_exists(self.driver, self.locators.PROFILE_SCREEN_TITLE, timeout=0.5)
                    or element_exists(self.driver, self.locators.PROFILE_LOGIN_BUTTON, timeout=0.5)
                )
                if on_profile:
                    self.tap_top_left_back()
                    try:
                        WebDriverWait(self.driver, 1).until(
                            EC.invisibility_of_element_located(self.locators.PROFILE_SCREEN_TITLE)
                        )
                    except Exception:
                        pass
                    logger.info("Profile: tapped back")
                    return True
        except Exception as e:
            logger.debug(f"Profile check: {e}")
        try:
            if self.driver.current_package == APP_PACKAGE:
                home_locators = (
                    HomePageLocators.HOME_INDICATOR,
                    HomePageLocators.HOME_TAB,
                    HomePageLocators.HOME_TAB_ALT,
                    HomePageLocators.SEARCH_CONTAINER,
                    HomePageLocators.SEARCH_CONTAINER_XPATH,
                )
                for loc in home_locators:
                    if element_exists(self.driver, loc, timeout=1.0):
                        return False
        except Exception:
            pass
        try:
            if self.driver.current_package == APP_PACKAGE:
                if self.tap_top_right_close():
                    try:
                        WebDriverWait(self.driver, 1).until(
                            EC.visibility_of_element_located(HomePageLocators.HOME_INDICATOR)
                        )
                    except Exception:
                        try:
                            WebDriverWait(self.driver, 1).until(
                                EC.visibility_of_element_located(HomePageLocators.SEARCH_CONTAINER)
                            )
                        except Exception:
                            pass
                    logger.info("Tapped top-right close (onboarding)")
                    return True
        except Exception as e:
            logger.debug(f"Top-right tap: {e}")
        locators_to_try = [
            self.locators.TOP_RIGHT_CLOSE_X,
            self.locators.TOP_RIGHT_CLOSE_X_DESC,
            self.locators.TOP_RIGHT_CLOSE_X_ICON,
            self.locators.ONBOARDING_CLOSE,
            self.locators.CLOSE_BUTTON,
            self.locators.PROFILE_BACK_ARROW,
            self.locators.PROFILE_BACK_NAVIGATE_UP,
            self.locators.PROFILE_BACK_XPATH,
            self.locators.ALLOW_BUTTON,
            self.locators.ALLOW_BUTTON_GOOGLE,
            self.locators.ALLOW_WHILE_USING,
            self.locators.SKIP_BUTTON,
            self.locators.SKIP_TEXT,
            self.locators.MAYBE_LATER,
            self.locators.NOT_NOW,
            self.locators.GET_STARTED,
            self.locators.NEXT_BUTTON,
            self.locators.CONTINUE_BTN,
            self.locators.LETS_GO,
        ]
        for locator in locators_to_try:
            if element_exists(self.driver, locator, timeout=1):
                if safe_click(self.driver, locator, timeout=2):
                    logger.info(f"Dismissed using {locator[0]}")
                    try:
                        WebDriverWait(self.driver, 1).until(
                            EC.invisibility_of_element_located(locator)
                        )
                    except Exception:
                        pass
                    return True
        return False

    def is_login_screen_visible(self, timeout: int = 4) -> bool:
        """Return True if the login/signup screen is visible (e.g. after Place Order)."""
        login_locs = [
            self.locators.PROFILE_LOGIN_BUTTON,
            self.locators.LOGIN_LOGIN_SIGNUP_TEXT,
            self.locators.LOGIN_LOGIN_SIGNUP_DESC,
            self.locators.LOGIN_SIGNIN_TEXT,
            self.locators.LOGIN_CONTINUE_PHONE,
            self.locators.LOGIN_MOBILE_HINT,
        ]
        for loc in login_locs:
            try:
                WebDriverWait(self.driver, timeout).until(
                    EC.visibility_of_element_located(loc)
                )
                return True
            except Exception:
                continue
        return False

    def handle_initial_popups(self, max_attempts: int = 5) -> None:
        """Repeatedly attempt to dismiss popups that appear on app launch until none remain."""
        for _ in range(max_attempts):
            if not self.dismiss_popup():
                break
            if HomePage(self.driver).wait_until_home_visible(timeout=1):
                break
