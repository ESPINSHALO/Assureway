#!/usr/bin/env python3
"""
Automate opening Myntra app: launch, handle popups, confirm home,
perform search, then keep app open or quit.

Flow: Launch → Handle popups → Confirm home (Home tab) → perform_search → Keep open → Quit.

Run:
  python scripts/open_myntra_home.py
  python scripts/open_myntra_home.py --stay   # Keep open until Ctrl+C

Prerequisites: Appium server running (appium), Android emulator with Myntra installed.
"""
import argparse
import sys
import time
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from core.driver_factory import create_driver, quit_driver
from pages.locators import HomePageLocators, SearchPageLocators, ProductPageLocators, BagPageLocators, PopupLocators
from pages.popup_handler import PopupHandler
from utils.logger import logger

MYNTRA_PACKAGE = "com.myntra.android"
TOP_RIGHT_TAP_SEC = 5       # Tap top-right X long enough to close first popup
POPUP_HANDLING_SEC = 2      # Brief popup check so we go to search within ~2 sec of Back
HOME_PAGE_WAIT_SEC = 0    # No extra wait — go to search immediately
KEEP_OPEN_AFTER_SEARCH_SEC = 15


def _current_package(driver):
    try:
        return driver.current_package
    except Exception:
        return None


def _close_running_screens_until_home(driver, popup_handler):
    """
    Dismiss popups so home is reached on first launch (no second app open).
    """
    logger.info(f"Popup handling: {POPUP_HANDLING_SEC} seconds...")
    start = time.time()
    no_dismiss_count = 0

    while (time.time() - start) < POPUP_HANDLING_SEC:
        current = _current_package(driver)
        if current == MYNTRA_PACKAGE:
            dismissed = popup_handler.dismiss_popup()
            if dismissed:
                no_dismiss_count = 0
                time.sleep(0.5)
                continue
            no_dismiss_count += 1
            if no_dismiss_count >= 2:
                if not popup_handler.dismiss_popup():
                    logger.info("Reached home screen.")
                    return True
                no_dismiss_count = 0
        else:
            popup_handler.dismiss_popup()
            time.sleep(0.5)
        time.sleep(0.5)

    return _current_package(driver) == MYNTRA_PACKAGE


def _dismiss_profile_if_open(driver) -> bool:
    """If profile page is open, press Back once to return to home. Returns True if back was pressed."""
    try:
        if driver.current_package != MYNTRA_PACKAGE:
            return False
        profile_title = driver.find_elements(*PopupLocators.PROFILE_SCREEN_TITLE)
        profile_login = driver.find_elements(*PopupLocators.PROFILE_LOGIN_BUTTON)
        if (profile_title and profile_title[0].is_displayed()) or (profile_login and profile_login[0].is_displayed()):
            driver.press_keycode(4)  # KEYCODE_BACK
            time.sleep(0.6)
            print("Profile page closed (Back once)")
            logger.info("Profile page closed (Back once)")
            return True
    except Exception:
        pass
    return False


def perform_search(driver, query: str, timeout: int = 5) -> None:
    """
    Pure Appium search. No ADB. Uses Myntra resource-ids first, then fallbacks.
    Raises if any required element is not found.
    """
    # If profile page interrupted, go back once
    _dismiss_profile_if_open(driver)

    # Locate search bar immediately (skip home check — we're already on home)
    search_container = None
    search_container_locators = [
        (AppiumBy.ID, "com.myntra.android:id/search_widget_text"),
        (AppiumBy.XPATH, "//*[@clickable='true' and .//*[contains(@text,'Jeans') or contains(@text,'Search')]]"),
        (AppiumBy.XPATH, "//*[contains(@text,'Jeans') or contains(@text,'Search') or contains(@content-desc,'Search')]"),
        (AppiumBy.ACCESSIBILITY_ID, "Search"),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("Search")'),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Jeans")'),
        (AppiumBy.CLASS_NAME, "android.widget.EditText"),
    ]
    # Short timeouts so we fail fast and try next locator (driver implicit_wait should be 0)
    wait_search = WebDriverWait(driver, 0.8)
    for by, value in search_container_locators:
        try:
            el = wait_search.until(EC.visibility_of_element_located((by, value)))
            if el and el.is_displayed():
                search_container = el
                break
        except Exception:
            continue
    if not search_container:
        raise Exception("Search container not found on home")
    print("Search container found")
    logger.info("Search container found.")

    # D. Click/tap the search container
    def _try_click_or_tap():
        try:
            search_container.click()
            print("[DEBUG] Search bar: element.click() used")
            return True
        except Exception as e:
            print(f"[DEBUG] element.click() failed: {e}")
        try:
            loc = search_container.location
            sz = search_container.size
            cx = loc["x"] + sz["width"] // 2
            cy = loc["y"] + sz["height"] // 2
            driver.tap([(cx, cy)])
            print(f"[DEBUG] Search bar: tapped at element center ({cx}, {cy})")
            return True
        except Exception as e2:
            print(f"[DEBUG] Tap at center failed: {e2}")
        return False

    _try_click_or_tap()
    time.sleep(1.5)

    # E. Wait for search screen (EditText). If not found, tap at typical search bar position.
    def _find_search_input():
        for by, value in [
            (AppiumBy.ID, "com.myntra.android:id/search_input"),
            (AppiumBy.CLASS_NAME, "android.widget.EditText"),
        ]:
            try:
                el = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((by, value))
                )
                if el and el.is_displayed():
                    return el
            except Exception:
                continue
        return None

    search_input = _find_search_input()

    # Fallback: tap at screen position where search bar usually is (below header, center)
    if not search_input:
        print("[DEBUG] Search screen did not open. Tapping at typical search bar position...")
        try:
            w, h = driver.get_window_size()["width"], driver.get_window_size()["height"]
            for y_ratio in [0.22, 0.25, 0.28]:
                tx, ty = w // 2, int(h * y_ratio)
                driver.tap([(tx, ty)])
                print(f"[DEBUG] Tapped at ({tx}, {ty}) = center, {int(y_ratio*100)}% from top")
                time.sleep(1.2)
                search_input = _find_search_input()
                if search_input:
                    break
        except Exception as e:
            print(f"[DEBUG] Position tap failed: {e}")
            logger.warning(f"Position tap: {e}")

    if not search_input:
        raise Exception("Search input field did not appear. Try Appium Inspector to get the exact locator for the search bar.")
    print("Search screen opened")
    logger.info("Search screen opened.")

    # F & G. Click inside EditText so we can type
    search_input.click()
    time.sleep(0.5)

    # H. Clear the field
    search_input.clear()
    time.sleep(0.3)

    # I. send_keys(query)
    print("Typing starts")
    logger.info("Typing starts.")
    search_input.send_keys(query)
    time.sleep(0.5)

    # J. Submit
    driver.press_keycode(66)
    time.sleep(1.5)

    # K. Wait for results page (listing/category page may use different structure than search_results_recycler)
    results_locators = [
        (AppiumBy.ID, "com.myntra.android:id/search_results_recycler"),
        (AppiumBy.CLASS_NAME, "androidx.recyclerview.widget.RecyclerView"),
        (AppiumBy.XPATH, "//*[contains(@resource-id, 'result')]"),
        SearchPageLocators.SORT_BUTTON,  # Shoes/category page has SORT at bottom
        (AppiumBy.XPATH, "//*[contains(@text,'SHOES') or contains(@text,'Shoes')]"),
    ]
    found = False
    for by, value in results_locators:
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((by, value)))
            found = True
            break
        except Exception:
            continue
    if found:
        print("Search results loaded")
        logger.info("Search results loaded.")
    else:
        # Don't raise — shoes/listing page often loads with different IDs; script continues to Sort + first shoe
        print("Results page may use different structure; continuing to Sort and first shoe.")
        logger.info("Results container not found by locator; continuing (listing page may use different structure).")


def sort_price_low_to_high_and_open_first_shoe(driver, select_male: bool = True) -> None:
    """On shoes listing: optional Gender → Male, then Sort → Discounts → tap first shoe."""
    wait = WebDriverWait(driver, 15)

    # Optional: select Gender → Male, wait for list to load
    if select_male:
        try:
            gender_btn = wait.until(EC.element_to_be_clickable(SearchPageLocators.GENDER_BUTTON))
            gender_btn.click()
            print("Gender button tapped")
            logger.info("Gender button tapped")
            time.sleep(1)
            male_opt = wait.until(EC.element_to_be_clickable(SearchPageLocators.GENDER_MALE))
            male_opt.click()
            print("Male selected")
            logger.info("Male selected")
            time.sleep(2)  # Wait for listing to load after gender filter
        except Exception as e:
            logger.warning(f"Gender Male: {e}")

    # Tap SORT button (e.g. "↓↑ SORT" at bottom)
    try:
        sort_btn = wait.until(EC.element_to_be_clickable(SearchPageLocators.SORT_BUTTON))
        sort_btn.click()
        print("Sort button tapped")
        logger.info("Sort button tapped")
    except Exception as e:
        logger.warning(f"Sort button: {e}")
        return
    time.sleep(1.5)  # Let sort bottom sheet fully open
    # Tap "Discounts" in the sort bottom sheet (Sort by page)
    discounts_clicked = False
    for discount_loc in [
        SearchPageLocators.SORT_DISCOUNTS,
        (AppiumBy.XPATH, "//*[contains(@text,'Discount') or contains(@text,'discount')]"),
        (AppiumBy.XPATH, "//*[contains(@content-desc,'Discount') or contains(@content-desc,'discount')]"),
        (AppiumBy.XPATH, "//*[starts-with(@text,'Discount') or @text='Discounts']"),
    ]:
        try:
            el = WebDriverWait(driver, 5).until(EC.element_to_be_clickable(discount_loc))
            if el and el.is_displayed():
                el.click()
                print("Discounts selected")
                logger.info("Discounts selected")
                discounts_clicked = True
                break
        except Exception as e:
            logger.debug(f"Discounts locator: {e}")
            continue
    if not discounts_clicked:
        logger.warning("Discounts option not found on sort page; continuing to first shoe.")
    time.sleep(2)
    try:
        size = driver.get_window_size()
        screen_w, screen_h = size["width"], size["height"]
    except Exception:
        screen_w, screen_h = 1080, 2400
    # First shoe = strip exactly above MEN/SORT/FILTER (no banner). Tap only in this band (78%–86% from top).
    strip_min_y = int(screen_h * 0.78)
    strip_max_y = int(screen_h * 0.86)

    # Tap only: left column, in the strip just above the gender section (first visible product row)
    for y_pct in [0.82, 0.80, 0.84, 0.79, 0.85]:
        try:
            x = int(screen_w * 0.25)
            y = int(screen_h * y_pct)
            if y < strip_min_y or y > strip_max_y:
                continue
            driver.tap([(x, y)])
            print("First shoe opened (tap above gender)")
            logger.info("First shoe opened (tap above gender)")
            return
        except Exception:
            continue
    for x_pct in [0.22, 0.28]:
        try:
            x = int(screen_w * x_pct)
            y = int(screen_h * 0.82)
            driver.tap([(x, y)])
            print("First shoe opened (tap above gender)")
            logger.info("First shoe opened (tap above gender)")
            return
        except Exception:
            continue
    logger.warning("Could not tap first shoe.")


def add_to_bag_select_available_size(driver) -> None:
    """On product page: click Add to bag → size pop-up opens → click available size → click DONE."""
    wait = WebDriverWait(driver, 15)
    time.sleep(2)

    # Step 1: Click "Add to bag" first — this opens the "Select Size (UK Size)" pop-up
    add_clicked = False
    for add_loc in [
        ProductPageLocators.ADD_TO_BAG,
        ProductPageLocators.ADD_TO_BAG_TEXT,
        ProductPageLocators.ADD_TO_BAG_DESC,
    ]:
        try:
            add_btn = wait.until(EC.element_to_be_clickable(add_loc))
            add_btn.click()
            print("Add to bag clicked (opens size pop-up)")
            logger.info("Add to bag clicked (opens size pop-up)")
            add_clicked = True
            break
        except Exception:
            continue
    if not add_clicked:
        try:
            sz = driver.get_window_size()
            w, h = sz["width"], sz["height"]
            driver.swipe(w // 2, int(h * 0.7), w // 2, int(h * 0.35), 400)
            time.sleep(0.5)
            for add_loc in [
                ProductPageLocators.ADD_TO_BAG,
                ProductPageLocators.ADD_TO_BAG_TEXT,
                ProductPageLocators.ADD_TO_BAG_DESC,
            ]:
                try:
                    add_btn = wait.until(EC.element_to_be_clickable(add_loc))
                    add_btn.click()
                    add_clicked = True
                    break
                except Exception:
                    continue
        except Exception:
            pass
    if not add_clicked:
        for y_ratio in [0.88, 0.90, 0.92]:
            try:
                sz = driver.get_window_size()
                w, h = sz["width"], sz["height"]
                driver.tap([(w // 2, int(h * y_ratio))])
                print("Add to bag tapped (opens size pop-up)")
                add_clicked = True
                break
            except Exception:
                pass

    if not add_clicked:
        logger.warning("Add to bag button not found; skipping size pop-up flow.")
        return

    time.sleep(1.5)  # Wait for Select Size pop-up to appear

    # Step 2: In the pop-up, click the first available size (try 5, then 6, 7, 8, 9, 10; only non-greyed are clickable)
    size_clicked = False
    for size_val in ["5", "6", "7", "8", "9", "10"]:
        try:
            # Prefer exact text so we hit the size chip (e.g. "5") not another element
            size_el = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((AppiumBy.XPATH, f"//*[@text='{size_val}']"))
            )
            if size_el and size_el.is_displayed():
                size_el.click()
                print(f"Available size {size_val} clicked")
                logger.info(f"Available size {size_val} clicked")
                size_clicked = True
                break
        except Exception:
            continue
    if not size_clicked:
        for size_val in ["5", "6", "7", "8", "9", "10"]:
            try:
                size_el = WebDriverWait(driver, 2).until(
                    EC.element_to_be_clickable(
                        (AppiumBy.XPATH, f"//*[contains(@text,'UK {size_val}') or contains(@text,'US {size_val}') or @text='{size_val}']")
                    )
                )
                if size_el and size_el.is_displayed():
                    size_el.click()
                    print(f"Available size {size_val} clicked")
                    size_clicked = True
                    break
            except Exception:
                continue
    if not size_clicked:
        try:
            any_size = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable(ProductPageLocators.SIZE_ANY)
            )
            any_size.click()
            print("Available size clicked (fallback)")
            size_clicked = True
        except Exception:
            pass

    time.sleep(0.8)

    # Step 3: Click DONE to confirm and add to bag
    done_clicked = False
    try:
        done_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(ProductPageLocators.SIZE_DONE_BUTTON)
        )
        done_btn.click()
        print("DONE clicked")
        logger.info("DONE clicked")
        done_clicked = True
    except Exception:
        pass
    if not done_clicked:
        try:
            done_btn = driver.find_element(AppiumBy.XPATH, "//*[contains(@text,'DONE') or contains(@text,'Done')]")
            done_btn.click()
            print("DONE clicked (fallback)")
            done_clicked = True
        except Exception as e:
            logger.warning(f"DONE button not found: {e}")
    if not done_clicked:
        # Fallback: tap bottom-center where DONE usually is (pink button at bottom of pop-up)
        try:
            sz = driver.get_window_size()
            w, h = sz["width"], sz["height"]
            driver.tap([(w // 2, int(h * 0.92))])
            print("DONE tapped (position)")
        except Exception:
            pass


def _return_to_home(driver, back_presses: int = 3, max_extra_back: int = 3) -> bool:
    """Press back 3 times (top-left) to return to home. If still not home, press back up to max_extra_back more."""
    def _is_home():
        try:
            return driver.find_element(*HomePageLocators.HOME_TAB).is_displayed()
        except Exception:
            pass
        try:
            return driver.find_element(*HomePageLocators.HOME_INDICATOR).is_displayed()
        except Exception:
            pass
        try:
            return driver.find_element(*HomePageLocators.HOME_TAB_ALT).is_displayed()
        except Exception:
            pass
        return False

    for _ in range(back_presses):
        try:
            driver.back()
            time.sleep(0.6)
        except Exception:
            break
    time.sleep(0.5)
    if _is_home():
        return True
    for _ in range(max_extra_back):
        try:
            driver.back()
            time.sleep(0.6)
        except Exception:
            break
        if _is_home():
            return True
    return False


def open_cart_increase_quantity_and_checkout(driver, quantity: int = 2) -> None:
    """After add to bag: return to home, click bottom-right bag icon to open cart, set quantity, Proceed to checkout."""
    wait = WebDriverWait(driver, 15)
    time.sleep(1.0)

    # Step 1: Return to home page (cancel top-right cart; use bottom nav bag instead)
    print("Returning to home page...")
    logger.info("Returning to home page...")
    if not _return_to_home(driver):
        logger.warning("Could not return to home; will try bottom bag icon anyway.")
    time.sleep(1.0)

    # Step 2: Click bottom-right bag (cart) icon in the bottom navigation bar
    bag_clicked = False
    try:
        bag_el = wait.until(EC.element_to_be_clickable(HomePageLocators.BAG_ICON))
        # Bottom nav: ensure we click the one at bottom (e.g. y in bottom 15% of screen)
        sz = driver.get_window_size()
        loc = bag_el.location
        if loc["y"] >= sz["height"] * 0.8:  # bottom 20%
            bag_el.click()
        else:
            # Same ID might be used elsewhere; tap bottom-right area for bag tab
            driver.tap([(int(sz["width"] * 0.92), int(sz["height"] * 0.96))])
        print("Bottom bag icon clicked")
        logger.info("Bottom bag icon clicked")
        bag_clicked = True
    except Exception as e:
        logger.debug(f"Bottom bag by element: {e}")
    if not bag_clicked:
        try:
            sz = driver.get_window_size()
            w, h = sz["width"], sz["height"]
            driver.tap([(int(w * 0.92), int(h * 0.96))])
            print("Bottom bag icon tapped (position)")
            bag_clicked = True
        except Exception:
            pass
    if not bag_clicked:
        logger.warning("Bottom bag icon not found; skipping quantity/checkout.")
        return

    time.sleep(2)  # Wait for bag/cart page to load

    # Step 3: Set quantity to `quantity` (e.g. 2) — click Qty dropdown, then select 2
    if quantity >= 2:
        qty_set = False
        # 3a: Click the Qty dropdown (e.g. "Qty: 1")
        for qty_loc in [
            BagPageLocators.QTY_DROPDOWN,
            (AppiumBy.XPATH, "//*[contains(@text,'Qty: 1') or contains(@text,'Qty : 1')]"),
            (AppiumBy.XPATH, "//*[contains(@text,'Qty')]"),
        ]:
            try:
                qty_el = WebDriverWait(driver, 4).until(EC.element_to_be_clickable(qty_loc))
                qty_el.click()
                print("Qty dropdown clicked")
                logger.info("Qty dropdown clicked")
                time.sleep(1.0)
                break
            except Exception:
                continue
        # 3b: Click option "2" in the dropdown
        try:
            opt = WebDriverWait(driver, 4).until(
                EC.element_to_be_clickable((AppiumBy.XPATH, "//*[@text='2']"))
            )
            opt.click()
            print("Quantity set to 2")
            logger.info("Quantity set to 2")
            qty_set = True
        except Exception:
            pass
        if not qty_set:
            try:
                opt = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable(BagPageLocators.QTY_OPTION_2)
                )
                opt.click()
                print("Quantity set to 2 (alt)")
                qty_set = True
            except Exception:
                pass
        if not qty_set:
            # Fallback: try plus button once (if UI has it)
            for plus_loc in [BagPageLocators.QUANTITY_PLUS, BagPageLocators.QUANTITY_PLUS_TEXT]:
                try:
                    plus_btn = WebDriverWait(driver, 3).until(EC.element_to_be_clickable(plus_loc))
                    plus_btn.click()
                    print("Quantity increased (+1)")
                    qty_set = True
                    break
                except Exception:
                    continue
        time.sleep(0.5)
        # 3c: Click DONE to confirm quantity and close dropdown
        try:
            done_btn = WebDriverWait(driver, 4).until(
                EC.element_to_be_clickable(ProductPageLocators.SIZE_DONE_BUTTON)
            )
            done_btn.click()
            print("DONE clicked (quantity confirmed)")
            logger.info("DONE clicked (quantity confirmed)")
        except Exception:
            try:
                done_btn = driver.find_element(AppiumBy.XPATH, "//*[contains(@text,'DONE') or contains(@text,'Done')]")
                done_btn.click()
                print("DONE clicked")
            except Exception:
                pass
        time.sleep(0.8)

    # Step 4: Click Place Order
    place_order_clicked = False
    for checkout_loc in [
        (AppiumBy.XPATH, "//*[contains(@text,'PLACE ORDER') or contains(@text,'Place Order')]"),
        (AppiumBy.ID, "com.myntra.android:id/checkout"),
        BagPageLocators.PROCEED_TO_CHECKOUT,
        (AppiumBy.XPATH, "//*[contains(@text,'Proceed to checkout') or contains(@text,'PROCEED TO CHECKOUT')]"),
    ]:
        try:
            btn = WebDriverWait(driver, 5).until(EC.element_to_be_clickable(checkout_loc))
            btn.click()
            print("Place Order clicked")
            logger.info("Place Order clicked")
            place_order_clicked = True
            break
        except Exception:
            continue
    if not place_order_clicked:
        try:
            sz = driver.get_window_size()
            w, h = sz["width"], sz["height"]
            driver.swipe(w // 2, int(h * 0.6), w // 2, int(h * 0.3), 300)
            time.sleep(0.5)
            btn = WebDriverWait(driver, 3).until(EC.element_to_be_clickable(BagPageLocators.PROCEED_TO_CHECKOUT))
            btn.click()
            place_order_clicked = True
        except Exception:
            pass
    if not place_order_clicked:
        try:
            driver.tap([(driver.get_window_size()["width"] // 2, int(driver.get_window_size()["height"] * 0.92))])
            print("Proceed to checkout tapped (position)")
        except Exception as e:
            logger.warning(f"Proceed to checkout not found: {e}")

    # Step 5: If login screen opens after Place Order, click X (top right) to close and return to home
    time.sleep(1.5)
    login_closed = False
    for close_loc in [
        PopupLocators.ONBOARDING_CLOSE,
        PopupLocators.CLOSE_BUTTON,
        PopupLocators.TOP_RIGHT_CLOSE_X,
        PopupLocators.TOP_RIGHT_CLOSE_X_DESC,
        (AppiumBy.XPATH, "//*[contains(@content-desc,'Close') or contains(@resource-id,'close')]"),
    ]:
        try:
            close_el = WebDriverWait(driver, 3).until(EC.element_to_be_clickable(close_loc))
            close_el.click()
            print("Login screen closed (X clicked)")
            logger.info("Login screen closed (X clicked)")
            login_closed = True
            break
        except Exception:
            continue
    if not login_closed:
        try:
            sz = driver.get_window_size()
            w, h = sz["width"], sz["height"]
            driver.tap([(int(w * 0.92), int(h * 0.08))])
            print("Login screen closed (top-right tap)")
            login_closed = True
        except Exception:
            pass
    if login_closed:
        time.sleep(0.8)
        _return_to_home(driver)

    # Step 6: Open cart again (bottom bag) and empty the cart
    time.sleep(1.0)
    bag_opened = False
    try:
        bag_el = WebDriverWait(driver, 4).until(
            EC.element_to_be_clickable(HomePageLocators.BAG_ICON)
        )
        sz = driver.get_window_size()
        loc = bag_el.location
        if loc.get("y", 0) >= sz["height"] * 0.8:
            bag_el.click()
        else:
            driver.tap([(int(sz["width"] * 0.92), int(sz["height"] * 0.96))])
        print("Cart opened again")
        logger.info("Cart opened again")
        bag_opened = True
    except Exception:
        try:
            driver.tap([(int(driver.get_window_size()["width"] * 0.92), int(driver.get_window_size()["height"] * 0.96))])
            bag_opened = True
        except Exception:
            pass
    if bag_opened:
        time.sleep(2.0)
        # Remove all items: try X on product card or trash/delete icon first, then generic remove
        while True:
            removed = False
            for remove_loc in [
                BagPageLocators.ITEM_CLOSE_X,
                BagPageLocators.ITEM_CLOSE_X_ALT,
                BagPageLocators.TRASH_DELETE_ICON,
                BagPageLocators.REMOVE_ITEM,
                BagPageLocators.REMOVE_ITEM_XPATH,
            ]:
                try:
                    remove_btn = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable(remove_loc)
                    )
                    remove_btn.click()
                    print("Remove item clicked (X or delete icon)")
                    removed = True
                    time.sleep(0.8)
                    for confirm_loc in [BagPageLocators.CONFIRM_REMOVE, BagPageLocators.CONFIRM_REMOVE_TEXT]:
                        try:
                            confirm_btn = WebDriverWait(driver, 3).until(
                                EC.element_to_be_clickable(confirm_loc)
                            )
                            confirm_btn.click()
                            print("Remove confirmed")
                            break
                        except Exception:
                            continue
                    break
                except Exception:
                    continue
            if not removed:
                # Fallback: tap top-right of first bag item (where X often is)
                try:
                    item = driver.find_element(*BagPageLocators.BAG_ITEMS)
                    loc = item.location
                    size = item.size
                    if loc and size:
                        tx = loc["x"] + size["width"] - 30
                        ty = loc["y"] + 30
                        driver.tap([(tx, ty)])
                        print("Remove tapped (X position on item)")
                        removed = True
                        time.sleep(0.8)
                        for confirm_loc in [BagPageLocators.CONFIRM_REMOVE, BagPageLocators.CONFIRM_REMOVE_TEXT]:
                            try:
                                confirm_btn = WebDriverWait(driver, 2).until(
                                    EC.element_to_be_clickable(confirm_loc)
                                )
                                confirm_btn.click()
                                break
                            except Exception:
                                continue
                except Exception:
                    pass
            if not removed:
                break
            time.sleep(1.0)
        print("Cart emptied")
        logger.info("Cart emptied")
        # Return to home after emptying cart
        time.sleep(0.8)
        _return_to_home(driver)


def main(stay_open: bool = False, select_male: bool = True) -> bool:
    """
    STEP 1: Launch app
    0–3 sec: Top-right close (X) — popup cancel
    4th sec: Home page (popup handler until home)
    5th sec: Click search bar
    6th sec: Type "shoes" and search
    STEP 5: Keep app open 15 sec (or --stay until Ctrl+C)
    STEP 6: Quit driver
    """
    driver = None
    try:
        # STEP 1: Launch app
        logger.info("STEP 1: Launch app")
        print("STEP 1: Launch app")
        driver = create_driver()

        # Wait for onboarding/splash so the X is visible, then tap long enough to close on first launch
        time.sleep(1.5)
        logger.info(f"Top-right close (X): running for {TOP_RIGHT_TAP_SEC} seconds...")
        print(f"Top-right close (X): {TOP_RIGHT_TAP_SEC} seconds...")

        w, h = 1080, 2400
        try:
            s = driver.get_window_size()
            w, h = s["width"], s["height"]
        except Exception:
            pass

        # Tap several positions in top-right so popup closes first time (no second open)
        x_positions = [
            (0.92, 0.08),
            (0.95, 0.07),
            (0.90, 0.08),
            (0.92, 0.06),
            (0.88, 0.08),
        ]
        end = time.time() + TOP_RIGHT_TAP_SEC
        tap_count = 0
        while time.time() < end:
            for x_ratio, y_ratio in x_positions:
                x, y = int(w * x_ratio), int(h * y_ratio)
                try:
                    driver.tap([(x, y)])
                    tap_count += 1
                except Exception as e:
                    logger.debug(f"Tap at ({x},{y}) failed: {e}")
            time.sleep(0.35)
        print(f"Top-right close done. ({tap_count} taps)")
        logger.info(f"Top-right X: {tap_count} taps attempted.")

        # Brief settle so first popup close takes effect before more dismissal
        time.sleep(0.8)

        # STEP 2: Handle any remaining popups (all in first launch, no second open)
        logger.info("STEP 2: Handle popups")
        print("STEP 2: Handle popups")
        popup = PopupHandler(driver)
        _close_running_screens_until_home(driver, popup)

        time.sleep(0.3)
        if _current_package(driver) != MYNTRA_PACKAGE:
            logger.warning("App may have left Myntra after popups; continuing without activate_app.")

        # No extra home wait — go straight to search
        if HOME_PAGE_WAIT_SEC > 0:
            time.sleep(HOME_PAGE_WAIT_SEC)

        # STEP 3: Confirm home quickly then search (short timeouts)
        logger.info("STEP 3: Confirm home → search")
        print("STEP 3: Confirm home → search")
        try:
            WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable(HomePageLocators.HOME_TAB)
            )
        except Exception:
            try:
                WebDriverWait(driver, 2).until(
                    EC.element_to_be_clickable(HomePageLocators.HOME_TAB_ALT)
                )
            except Exception:
                pass
        time.sleep(0.2)

        # STEP 4: Search immediately (don't add extra delay)
        logger.info("STEP 4: Click search bar, type shoes, search")
        print("STEP 4: Search (click bar → type shoes → search)")
        perform_search(driver, "shoes")

        # STEP 4b: Gender Male (optional) → Sort → Discounts → open first shoe
        logger.info("STEP 4b: Gender Male (if enabled) → Sort → Discounts → first shoe")
        print("STEP 4b: Gender Male → Sort → Discounts → first shoe")
        sort_price_low_to_high_and_open_first_shoe(driver, select_male=select_male)
        time.sleep(1.5)

        # STEP 4c: On product page — select any available size (6–10), then Add to bag
        logger.info("STEP 4c: Select available size (6,7,8,9,10), Add to bag")
        print("STEP 4c: Select available size → Add to bag")
        add_to_bag_select_available_size(driver)
        time.sleep(1)

        # STEP 4d: Return to home → click bottom-right bag icon → quantity 2 → Proceed to checkout
        logger.info("STEP 4d: Home → bottom bag → quantity 2 → Proceed to checkout")
        print("STEP 4d: Return to home → bottom bag → quantity 2 → Proceed to checkout")
        open_cart_increase_quantity_and_checkout(driver, quantity=2)
        time.sleep(1)

        # STEP 5: Keep app open 15 seconds after search completes
        if stay_open:
            logger.info("STEP 5: Keeping app open until Ctrl+C (--stay)")
            print("STEP 5: App open. Press Ctrl+C to close.")
            while True:
                time.sleep(1)
        else:
            logger.info(f"STEP 5: Keeping app open for {KEEP_OPEN_AFTER_SEARCH_SEC} seconds...")
            print(f"STEP 5: Keeping app open for {KEEP_OPEN_AFTER_SEARCH_SEC} seconds...")
            time.sleep(KEEP_OPEN_AFTER_SEARCH_SEC)

        # STEP 6: Clean quit
        logger.info("STEP 6: Quit driver")
        print("STEP 6: Quit driver")
        return True

    except KeyboardInterrupt:
        logger.info("Interrupted by user (Ctrl+C).")
        print("Interrupted by user.")
        return True
    except Exception as e:
        logger.error(f"Script failed: {e}")
        print(f"Error: {e}")
        raise  # Do not allow silent failure
    finally:
        if driver:
            quit_driver(driver)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Myntra automation: launch, popups, home, search, shoes.")
    parser.add_argument(
        "--stay",
        action="store_true",
        help="Keep app open; do not quit driver until Ctrl+C",
    )
    parser.add_argument(
        "--no-male",
        action="store_true",
        help="Skip selecting Gender = Male on shoes page (default: select Male)",
    )
    args = parser.parse_args()
    try:
        success = main(stay_open=args.stay, select_male=not args.no_male)
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"Fatal: {e}")
        logger.error(f"Fatal: {e}")
        sys.exit(1)
