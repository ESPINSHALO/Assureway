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


def _tap_at(driver, x: int, y: int) -> bool:
    """Perform a reliable tap at (x, y). Tries mobile gesture then W3C actions then tap()."""
    try:
        driver.execute_script("mobile: clickGesture", {"x": int(x), "y": int(y)})
        return True
    except Exception:
        pass
    try:
        driver.execute_script("mobile: tap", {"x": int(x), "y": int(y)})
        return True
    except Exception:
        pass
    try:
        from selenium.webdriver.common.actions.pointer_input import PointerInput
        from selenium.webdriver.common.actions.action_builder import ActionBuilder
        try:
            from selenium.webdriver.common.actions.interaction import POINTER_TOUCH
            kind = POINTER_TOUCH
        except ImportError:
            kind = "touch"
        actions = ActionBuilder(driver)
        pointer = PointerInput(kind, "finger")
        actions.add_pointer_input(pointer)
        actions.pointer_action.move_to_location(x, y)
        actions.pointer_action.pointer_down()
        actions.pointer_action.pointer_up()
        actions.perform()
        return True
    except Exception:
        pass
    try:
        driver.tap([(int(x), int(y))])
        return True
    except Exception:
        pass
    return False


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
    time.sleep(0.35)

    # E. Wait for search screen (EditText).
    def _find_search_input():
        wait_inp = WebDriverWait(driver, 0.8)
        for by, value in [
            (AppiumBy.ID, "com.myntra.android:id/search_input"),
            (AppiumBy.CLASS_NAME, "android.widget.EditText"),
        ]:
            try:
                el = wait_inp.until(
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
                time.sleep(0.5)
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
    time.sleep(0.2)

    # H. Clear the field
    search_input.clear()
    time.sleep(0.1)

    # I. send_keys(query)
    search_input.send_keys(query)
    time.sleep(0.2)

    # J. Submit
    driver.press_keycode(66)
    time.sleep(0.8)

    # K. Wait for results page (short timeout so we don't block 10s per locator)
    results_locators = [
        (AppiumBy.ID, "com.myntra.android:id/search_results_recycler"),
        (AppiumBy.CLASS_NAME, "androidx.recyclerview.widget.RecyclerView"),
        (AppiumBy.XPATH, "//*[contains(@resource-id, 'result')]"),
        SearchPageLocators.SORT_BUTTON,  # Shoes/category page has SORT at bottom
        (AppiumBy.XPATH, "//*[contains(@text,'SHOES') or contains(@text,'Shoes')]"),
    ]
    found = False
    wait_results = WebDriverWait(driver, 4)
    for by, value in results_locators:
        try:
            wait_results.until(EC.presence_of_element_located((by, value)))
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
    wait = WebDriverWait(driver, 8)

    # Optional: select Gender → Male, wait for list to load
    if select_male:
        try:
            gender_btn = wait.until(EC.element_to_be_clickable(SearchPageLocators.GENDER_BUTTON))
            gender_btn.click()
            print("Gender button tapped")
            logger.info("Gender button tapped")
            time.sleep(0.5)
            male_opt = wait.until(EC.element_to_be_clickable(SearchPageLocators.GENDER_MALE))
            male_opt.click()
            print("Male selected")
            logger.info("Male selected")
            time.sleep(1.0)  # Brief wait for listing after gender filter
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
    time.sleep(0.8)  # Let sort bottom sheet open
    # Tap "Discounts" in the sort bottom sheet (Sort by page)
    discounts_clicked = False
    wait_disc = WebDriverWait(driver, 3)
    for discount_loc in [
        SearchPageLocators.SORT_DISCOUNTS,
        (AppiumBy.XPATH, "//*[contains(@text,'Discount') or contains(@text,'discount')]"),
        (AppiumBy.XPATH, "//*[contains(@content-desc,'Discount') or contains(@content-desc,'discount')]"),
        (AppiumBy.XPATH, "//*[starts-with(@text,'Discount') or @text='Discounts']"),
    ]:
        try:
            el = wait_disc.until(EC.element_to_be_clickable(discount_loc))
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
    time.sleep(0.6)
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
    wait = WebDriverWait(driver, 8)
    time.sleep(0.8)

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
            time.sleep(0.3)
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

    time.sleep(0.6)  # Brief wait for Select Size pop-up

    # Step 2: In the pop-up, click the first available size (try 5, then 6, 7, 8, 9, 10; only non-greyed are clickable)
    size_clicked = False
    wait_size = WebDriverWait(driver, 2)
    for size_val in ["5", "6", "7", "8", "9", "10"]:
        try:
            # Prefer exact text so we hit the size chip (e.g. "5") not another element
            size_el = wait_size.until(
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
                size_el = wait_size.until(
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
            any_size = wait_size.until(
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
        done_btn = WebDriverWait(driver, 3).until(
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
            time.sleep(0.35)
        except Exception:
            break
    time.sleep(0.25)
    if _is_home():
        return True
    for _ in range(max_extra_back):
        try:
            driver.back()
            time.sleep(0.35)
        except Exception:
            break
        if _is_home():
            return True
    return False


def empty_cart_and_return_home(driver) -> None:
    """
    On Shopping Bag page: click product-card X (not header), confirm REMOVE in popup,
    wait until cart is empty, then return to Home screen.
    """
    wait_short = WebDriverWait(driver, 3)
    wait10 = WebDriverWait(driver, 10)

    # Step 1 — Detect Shopping Bag screen (any of: product card, title, ITEMS SELECTED, PLACE ORDER)
    bag_detected = False
    for loc in [
        BagPageLocators.BAG_ITEMS,
        BagPageLocators.BAG_SCREEN_TITLE,
        BagPageLocators.BAG_SCREEN_ITEMS_SELECTED,
        BagPageLocators.QTY_DROPDOWN,
        (AppiumBy.XPATH, "//*[contains(@text,'PLACE ORDER') or contains(@text,'Place Order')]"),
    ]:
        try:
            wait_short.until(EC.visibility_of_element_located(loc))
            bag_detected = True
            logger.info("Shopping bag detected")
            break
        except Exception:
            continue
    if not bag_detected:
        logger.warning("Shopping bag screen not detected")
        return

    # Step 2 — Click the product remove (X) icon: top-right of card, often last ImageView in card
    remove_icon = None
    for loc in [
        BagPageLocators.ITEM_CLOSE_X_LAST_IMAGE,
        BagPageLocators.ITEM_CLOSE_X_BY_SIZE_CARD,
        BagPageLocators.ITEM_CLOSE_X_LAST_CLICKABLE,
        BagPageLocators.REMOVE_ITEM,
        BagPageLocators.ITEM_CLOSE_X_FIRST_CARD,
        BagPageLocators.ITEM_CLOSE_X,
        (AppiumBy.XPATH, "(//*[contains(@resource-id,'bag_item')])[1]//android.widget.ImageButton"),
        (AppiumBy.XPATH, "//android.widget.ImageView[contains(@content-desc,'Close') or contains(@content-desc,'close')]"),
        BagPageLocators.TRASH_DELETE_ICON,
        (AppiumBy.XPATH, "(//*[contains(@resource-id,'bag_item')])[1]//android.widget.ImageView"),
        (AppiumBy.XPATH, "//android.widget.ImageView[contains(@content-desc,'Remove') or contains(@content-desc,'Delete')]"),
    ]:
        try:
            remove_icon = wait_short.until(EC.element_to_be_clickable(loc))
            break
        except Exception:
            continue
    if not remove_icon:
        # Fallback: use Qty/Size row to find card, then reliable tap at top-right (X)
        try:
            card_anchor = wait_short.until(
                EC.presence_of_element_located(
                    (AppiumBy.XPATH, "//*[contains(@text,'Qty:') or contains(@text,'Size:')]")
                )
            )
            loc, sz = card_anchor.location, card_anchor.size
            w, h = driver.get_window_size()["width"], driver.get_window_size()["height"]
            tx = w - 45
            # X is on the product card (below "1/1 ITEMS SELECTED" + Share/Trash/Heart). Tap in card title row only.
            # Use smaller offset so we don't hit the Heart/Trash row above the card.
            ty = max(loc["y"] - 200, 200)
            if not _tap_at(driver, tx, ty):
                ty = max(loc["y"] - 170, 200)
                _tap_at(driver, tx, ty)
            time.sleep(0.3)
            logger.info("Remove icon clicked (card top-right via Qty/Size)")
        except Exception:
            try:
                card = wait_short.until(EC.presence_of_element_located(BagPageLocators.BAG_ITEMS))
                loc, sz = card.location, card.size
                tx = loc["x"] + sz["width"] - 20
                ty = loc["y"] + 20
                _tap_at(driver, tx, ty)
                logger.info("Remove icon clicked (card top-right)")
            except Exception as e:
                logger.warning(f"Remove icon not found on Shopping Bag screen: {e}")
                return
    else:
        try:
            remove_icon.click()
            logger.info("Remove icon clicked")
        except Exception as e:
            logger.warning(f"Failed to click remove icon: {e}")
            return

    # Step 3 — Handle confirmation popup: click REMOVE (wait for popup then reliable tap)
    time.sleep(1.0)
    remove_button = None
    wait_popup = WebDriverWait(driver, 6)
    for loc in [
        (AppiumBy.XPATH, "//*[@text='REMOVE' or @text='Remove' or contains(@text,'REMOVE') or contains(@text,'Remove')]"),
        BagPageLocators.POPUP_REMOVE_BUTTON,
        BagPageLocators.CONFIRM_REMOVE_TEXT,
        BagPageLocators.CONFIRM_REMOVE,
        (AppiumBy.XPATH, "//android.widget.Button[contains(@text,'REMOVE') or contains(@text,'Remove')]"),
        (AppiumBy.XPATH, "//android.widget.TextView[contains(@text,'REMOVE') or contains(@text,'Remove')]"),
        (AppiumBy.XPATH, "//*[contains(@resource-id,'remove') or contains(@resource-id,'confirm')]"),
    ]:
        try:
            remove_button = wait_popup.until(EC.presence_of_element_located(loc))
            if remove_button and remove_button.is_displayed():
                break
        except Exception:
            continue
    if remove_button:
        try:
            try:
                rect = remove_button.rect
                cx = rect["x"] + rect["width"] // 2
                cy = rect["y"] + rect["height"] // 2
            except Exception:
                loc, sz = remove_button.location, remove_button.size
                cx = loc["x"] + sz["width"] // 2
                cy = loc["y"] + sz["height"] // 2
            if _tap_at(driver, cx, cy):
                logger.info("Remove confirmed from popup")
            else:
                remove_button.click()
                logger.info("Remove confirmed from popup")
        except Exception:
            try:
                remove_button.click()
                logger.info("Remove confirmed from popup")
            except Exception as e:
                logger.warning(f"Failed to click REMOVE on popup: {e}")
    else:
        w, h = driver.get_window_size()["width"], driver.get_window_size()["height"]
        for px, py in [(w // 2, int(h * 0.58)), (w // 2, int(h * 0.62)), (int(w * 0.75), int(h * 0.58)), (w // 2, int(h * 0.55))]:
            if _tap_at(driver, px, py):
                logger.info("Remove confirmed from popup (tap)")
                break
            time.sleep(0.2)

    # Step 4 — Wait for cart to be empty
    cart_emptied = False
    try:
        # Primary: product card disappears
        wait10.until(EC.invisibility_of_element_located(BagPageLocators.BAG_ITEMS))
        cart_emptied = True
    except Exception:
        # Fallback A: explicit empty-cart message
        try:
            wait10.until(EC.visibility_of_element_located(BagPageLocators.EMPTY_BAG_MESSAGE))
            cart_emptied = True
        except Exception:
            # Fallback B: PLACE ORDER button disappears (no items to order)
            try:
                wait10.until(
                    EC.invisibility_of_element_located(
                        (AppiumBy.XPATH, "//*[contains(@text,'PLACE ORDER') or contains(@text,'Place Order')]")
                    )
                )
                cart_emptied = True
            except Exception as e:
                logger.warning(f"Cart may not be fully empty after REMOVE: {e}")

    if cart_emptied:
        logger.info("Cart emptied successfully")

    # Step 5 — Return to Home screen: press Back until Home tab is visible
    def _on_home():
        for loc in [HomePageLocators.HOME_TAB, HomePageLocators.HOME_TAB_ALT]:
            try:
                return driver.find_element(*loc).is_displayed()
            except Exception:
                continue
        return False

    for _ in range(4):
        if _on_home():
            logger.info("Returned to home screen")
            return
        try:
            driver.back()
            time.sleep(0.3)
        except Exception:
            break
    if _on_home():
        logger.info("Returned to home screen")
    else:
        logger.warning("Home screen not confirmed after emptying cart")


def open_cart_increase_quantity_and_checkout(driver, quantity: int = 2) -> None:
    """After add to bag: return to home, click bottom-right bag icon to open cart, set quantity, Proceed to checkout."""
    wait = WebDriverWait(driver, 8)
    time.sleep(0.4)

    # Step 1: Return to home page (cancel top-right cart; use bottom nav bag instead)
    print("Returning to home page...")
    logger.info("Returning to home page...")
    if not _return_to_home(driver):
        logger.warning("Could not return to home; will try bottom bag icon anyway.")
    time.sleep(0.5)

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

    time.sleep(0.8)  # Brief wait for bag/cart page

    # Step 3: Set quantity to `quantity` (e.g. 2) — click Qty dropdown, then select 2
    if quantity >= 2:
        qty_set = False
        wait_qty = WebDriverWait(driver, 2)
        # 3a: Click the Qty dropdown (e.g. "Qty: 1")
        for qty_loc in [
            BagPageLocators.QTY_DROPDOWN,
            (AppiumBy.XPATH, "//*[contains(@text,'Qty: 1') or contains(@text,'Qty : 1')]"),
            (AppiumBy.XPATH, "//*[contains(@text,'Qty')]"),
        ]:
            try:
                qty_el = wait_qty.until(EC.element_to_be_clickable(qty_loc))
                qty_el.click()
                print("Qty dropdown clicked")
                logger.info("Qty dropdown clicked")
                time.sleep(0.5)
                break
            except Exception:
                continue
        # 3b: Click option "2" in the dropdown
        try:
            opt = wait_qty.until(
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
                opt = wait_qty.until(
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
                    plus_btn = wait_qty.until(EC.element_to_be_clickable(plus_loc))
                    plus_btn.click()
                    print("Quantity increased (+1)")
                    qty_set = True
                    break
                except Exception:
                    continue
        time.sleep(0.2)
        # 3c: Click DONE to confirm quantity and close dropdown
        try:
            done_btn = WebDriverWait(driver, 2).until(
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
        time.sleep(0.4)

    # Step 4: Click Place Order
    place_order_clicked = False
    wait_checkout = WebDriverWait(driver, 3)
    for checkout_loc in [
        (AppiumBy.XPATH, "//*[contains(@text,'PLACE ORDER') or contains(@text,'Place Order')]"),
        (AppiumBy.ID, "com.myntra.android:id/checkout"),
        BagPageLocators.PROCEED_TO_CHECKOUT,
        (AppiumBy.XPATH, "//*[contains(@text,'Proceed to checkout') or contains(@text,'PROCEED TO CHECKOUT')]"),
    ]:
        try:
            btn = wait_checkout.until(EC.element_to_be_clickable(checkout_loc))
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
            time.sleep(0.3)
            btn = wait_checkout.until(EC.element_to_be_clickable(BagPageLocators.PROCEED_TO_CHECKOUT))
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
    time.sleep(0.8)
    login_closed = False
    wait_close = WebDriverWait(driver, 2)
    for close_loc in [
        PopupLocators.ONBOARDING_CLOSE,
        PopupLocators.CLOSE_BUTTON,
        PopupLocators.TOP_RIGHT_CLOSE_X,
        PopupLocators.TOP_RIGHT_CLOSE_X_DESC,
        (AppiumBy.XPATH, "//*[contains(@content-desc,'Close') or contains(@resource-id,'close')]"),
    ]:
        try:
            close_el = wait_close.until(EC.element_to_be_clickable(close_loc))
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
        time.sleep(0.5)
        _return_to_home(driver)
        # Let home screen settle so bottom nav (bag icon) is ready
        try:
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located(HomePageLocators.HOME_TAB))
        except Exception:
            pass
        time.sleep(1.0)

    # Step 6: Open cart again (bottom bag), wait for Shopping Bag screen, then empty cart
    logger.info("Opening cart to empty it...")
    cart_opened = False
    for bag_loc in [
        HomePageLocators.BAG_ICON,
        (AppiumBy.ACCESSIBILITY_ID, "Bag"),
        (AppiumBy.XPATH, "//*[contains(@content-desc,'Bag') or contains(@content-desc,'Cart')]"),
    ]:
        try:
            bag_el = WebDriverWait(driver, 8).until(EC.element_to_be_clickable(bag_loc))
            bag_el.click()
            cart_opened = True
            print("Cart opened again")
            logger.info("Cart opened again")
            break
        except Exception:
            continue
    if not cart_opened:
        try:
            w, h = driver.get_window_size()["width"], driver.get_window_size()["height"]
            driver.tap([(int(w * 0.92), int(h * 0.96))])
            print("Cart opened (tap bottom-right)")
            logger.info("Cart opened (tap bottom-right)")
            cart_opened = True
        except Exception:
            pass
    if cart_opened:
        time.sleep(1.0)
        empty_cart_and_return_home(driver)
    else:
        logger.warning("Could not reopen cart to empty it")


def main(stay_open: bool = False, select_male: bool = True) -> bool:
    """
    STEP 1: Launch app
    ~1s: Press Back once to reach home
    2s: Click search bar and type "shoes"
    STEP 5: Keep app open 15 sec (or --stay until Ctrl+C)
    STEP 6: Quit driver
    """
    driver = None
    try:
        # STEP 1: Launch app
        logger.info("STEP 1: Launch app")
        print("STEP 1: Launch app")
        driver = create_driver()
        start_time = time.time()

        # Wait for first screen (onboarding/splash) to show before Back — too early and Back can exit the app
        time.sleep(2.5)
        logger.info("Press Back once to reach home...")
        print("Back once → home")
        try:
            driver.press_keycode(4)  # KEYCODE_BACK
        except Exception as e:
            logger.warning(f"Back key: {e}")
        time.sleep(0.4)

        # Then go to search bar and type shoes
        elapsed = time.time() - start_time
        wait_until_3s = max(0, 3.0 - elapsed)
        if wait_until_3s > 0:
            time.sleep(wait_until_3s)
        logger.info("Click search bar, type shoes")
        print("Click search bar → type shoes")
        perform_search(driver, "shoes")

        # STEP 4b: Gender Male (optional) → Sort → Discounts → open first shoe
        logger.info("STEP 4b: Gender Male (if enabled) → Sort → Discounts → first shoe")
        print("STEP 4b: Gender Male → Sort → Discounts → first shoe")
        sort_price_low_to_high_and_open_first_shoe(driver, select_male=select_male)
        time.sleep(0.8)

        # STEP 4c: On product page — select any available size (6–10), then Add to bag
        logger.info("STEP 4c: Select available size (6,7,8,9,10), Add to bag")
        print("STEP 4c: Select available size → Add to bag")
        add_to_bag_select_available_size(driver)
        time.sleep(0.5)

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
        if driver:
            print("Keeping app open 5s before exit...")
            time.sleep(5)
        raise
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
