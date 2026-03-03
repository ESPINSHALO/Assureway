"""Handles popups and dialogs (onboarding, login prompts)."""
from appium.webdriver.webdriver import WebDriver
from pages.base_page import BasePage
from pages.locators import PopupLocators, HomePageLocators
from utils.waits import element_exists, safe_click
from utils.logger import logger
import time


class PopupHandler(BasePage):
    """Handles dismissible popups."""

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        self.locators = PopupLocators()

    def dismiss_popup(self) -> bool:
        """
        Try to dismiss popups. Profile Back first (quick), then onboarding X.
        """
        # FIRST: Profile page – press Back immediately (don't waste time on top-right X)
        try:
            if self.driver.current_package == "com.myntra.android":
                on_profile = (
                    element_exists(self.driver, self.locators.PROFILE_SCREEN_TITLE, timeout=0.5)
                    or element_exists(self.driver, self.locators.PROFILE_LOGIN_BUTTON, timeout=0.5)
                )
                if on_profile:
                    self.tap_top_left_back()
                    time.sleep(0.3)
                    logger.info("Profile: tapped back")
                    return True
        except Exception as e:
            logger.debug(f"Profile check: {e}")

        # If already on HOME – do NOT tap top-right (that would open Profile)
        try:
            if self.driver.current_package == "com.myntra.android":
                on_home = element_exists(self.driver, HomePageLocators.HOME_INDICATOR, timeout=0.5)
                if on_home:
                    return False
        except Exception:
            pass

        # Onboarding only: top-right X (not when on home)
        try:
            if self.driver.current_package == "com.myntra.android":
                if self.tap_top_right_close():
                    time.sleep(0.5)
                    logger.info("Tapped top-right close (onboarding)")
                    return True
        except Exception as e:
            logger.debug(f"Top-right tap: {e}")

        locators_to_try = [
            # Onboarding X by locator (if element has content-desc/resource-id)
            self.locators.TOP_RIGHT_CLOSE_X,
            self.locators.TOP_RIGHT_CLOSE_X_DESC,
            self.locators.TOP_RIGHT_CLOSE_X_ICON,
            self.locators.ONBOARDING_CLOSE,
            self.locators.CLOSE_BUTTON,
            # Profile screen – back arrow to close and return to home
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
                    time.sleep(0.5)
                    return True
        return False

    def handle_initial_popups(self, max_attempts: int = 5) -> None:
        """
        Repeatedly try to dismiss popups that may appear on app launch.
        """
        for _ in range(max_attempts):
            if not self.dismiss_popup():
                break
            time.sleep(0.5)
