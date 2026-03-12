"""
Centralized element locators for the Myntra Android app.

Purpose: Holds all (By, value) tuples for home, search, product, bag, and popup screens.
Role: Keeps locators out of tests and page logic; single place to update when UI changes.
Architecture: Used by page classes in this package; update via Appium Inspector when IDs change.
"""
from appium.webdriver.common.appiumby import AppiumBy


class HomePageLocators:
    """Locators for the Myntra home screen: bottom nav, search bar, bag icon, profile."""
    HOME_TAB = (AppiumBy.XPATH, "//*[contains(@text, 'Home') and (contains(@content-desc, 'Home') or contains(@resource-id, 'home') or .//*[contains(@text, 'Home')])]")
    HOME_TAB_ALT = (AppiumBy.XPATH, "//*[@text='Home']")
    SEARCH_CONTAINER = (AppiumBy.ID, "com.myntra.android:id/search_widget_text")
    SEARCH_CONTAINER_XPATH = (AppiumBy.XPATH, "//*[contains(@resource-id, 'search') and (contains(@content-desc, 'Search') or .//*[@text])]")
    SEARCH_BAR_PLACEHOLDER = (AppiumBy.XPATH, "//*[contains(@text,'Jeans') or contains(@text,'Search') or contains(@content-desc,'Search')]")
    HOME_INDICATOR = (AppiumBy.XPATH, "//*[contains(@text, 'Add Delivery Address') or contains(@text, 'Delivery') or contains(@text, 'Earrings') or contains(@text, 'Search for') or contains(@text, 'Jeans')]")
    SEARCH_ICON = (AppiumBy.ID, "com.myntra.android:id/search_widget_text")
    BAG_ICON = (AppiumBy.ID, "com.myntra.android:id/cart_count")
    BAG_ICON_ACCESSIBILITY = (AppiumBy.ACCESSIBILITY_ID, "Bag")
    BAG_ICON_XPATH = (AppiumBy.XPATH, "//*[contains(@content-desc,'Bag') or contains(@content-desc,'Cart')]")
    PROFILE_ICON = (AppiumBy.ID, "com.myntra.android:id/profile")
    SEARCH_ACCESSIBILITY_ID = (AppiumBy.ACCESSIBILITY_ID, "Search")


class SearchPageLocators:
    """Locators for search input, results, listing filters (Gender, Sort), and first product card."""
    SEARCH_INPUT = (AppiumBy.ID, "com.myntra.android:id/search_input")
    SEARCH_INPUT_EDIT = (AppiumBy.CLASS_NAME, "android.widget.EditText")
    SEARCH_INPUT_PLACEHOLDER_JEANS = (AppiumBy.XPATH, "//android.widget.EditText[contains(@text, 'Jeans') or contains(@text, 'Earrings') or contains(@text, 'Search') or contains(@hint, 'Jeans') or contains(@content-desc, 'Search')]")
    SEARCH_INPUT_EDIT_XPATH = (AppiumBy.XPATH, "//android.widget.EditText")
    SEARCH_RESULTS_LIST = (AppiumBy.ID, "com.myntra.android:id/search_results_recycler")
    SEARCH_RESULTS_XPATH = (AppiumBy.XPATH, "//*[contains(@resource-id, 'search') and contains(@resource-id, 'result')]")
    FIRST_PRODUCT = (AppiumBy.XPATH, "//androidx.recyclerview.widget.RecyclerView//android.view.ViewGroup[1]")
    GENDER_BUTTON = (AppiumBy.XPATH, "//*[contains(@text,'GENDER') or contains(@text,'Gender')]")
    GENDER_MALE = (AppiumBy.XPATH, "//*[contains(@text,'Male') or contains(@text,'MALE') or @text='Men']")
    SORT_BUTTON = (AppiumBy.XPATH, "//*[contains(@text,'SORT') or contains(@text,'Sort')]")
    SORT_PRICE_HIGH_TO_LOW = (AppiumBy.XPATH, "//*[contains(@text,'Price - high to low') or contains(@text,'Price - High to Low') or contains(@text,'high to low')]")
    SORT_WHATS_NEW = (AppiumBy.XPATH, "//*[contains(@text,\"What's New\") or contains(@text,'Whats New') or contains(@text,'WHAT\'S NEW')]")
    SORT_DISCOUNTS = (AppiumBy.XPATH, "//*[contains(@text,'Discount') or contains(@text,'discount') or contains(@text,'DISCOUNT')]")
    FIRST_GENDER_SHOE_TOP_RATED = (AppiumBy.XPATH, "//*[contains(@text,'Top Rated')]/ancestor::*[@clickable='true'][1]")
    FIRST_PRODUCT_GRID_ITEM = (AppiumBy.XPATH, "(//androidx.recyclerview.widget.RecyclerView)[2]//android.view.ViewGroup[.//android.widget.ImageView][3]")
    FIRST_PRODUCT_GRID_ITEM_ALT = (AppiumBy.XPATH, "(//androidx.recyclerview.widget.RecyclerView)[2]//android.view.ViewGroup[.//android.widget.ImageView][4]")
    FIRST_PRODUCT_GRID_FROM_THIRD = (AppiumBy.XPATH, "(//androidx.recyclerview.widget.RecyclerView)[3]//android.view.ViewGroup[.//android.widget.ImageView][1]")
    FIRST_PRODUCT_CARD = (AppiumBy.XPATH, "(//androidx.recyclerview.widget.RecyclerView)[2]//android.view.ViewGroup[3]")
    FIRST_PRODUCT_CARD_ALT = (AppiumBy.XPATH, "(//androidx.recyclerview.widget.RecyclerView)[2]//android.view.ViewGroup[4]")
    FIRST_SHOE_PRODUCT = (AppiumBy.XPATH, "(//*[contains(@resource-id,'product') or contains(@resource-id,'plp')])[2]")


class ProductPageLocators:
    """Locators for product detail: size selector, Add to bag, size popup DONE, Go to bag."""
    SIZE_BUTTON = (AppiumBy.ID, "com.myntra.android:id/select_size")
    SIZE_OPTION = (AppiumBy.XPATH, "//android.widget.TextView[contains(@text, 'UK') or contains(@text, 'US')]")
    SIZE_ANY = (AppiumBy.XPATH, "//*[@text='5' or @text='6' or @text='7' or @text='8' or @text='9' or @text='10' or contains(@text,'UK 5') or contains(@text,'UK 6') or contains(@text,'UK 7') or contains(@text,'UK 8') or contains(@text,'UK 9') or contains(@text,'UK 10') or contains(@text,'US 5') or contains(@text,'US 6') or contains(@text,'US 7') or contains(@text,'US 8') or contains(@text,'US 9') or contains(@text,'US 10')]")
    SELECT_SIZE = (AppiumBy.XPATH, "//*[contains(@text,'Select Size') or contains(@text,'SELECT SIZE')]")
    ADD_TO_BAG = (AppiumBy.ID, "com.myntra.android:id/add_to_bag")
    ADD_TO_BAG_TEXT = (AppiumBy.XPATH, "//*[contains(@text,'ADD TO BAG') or contains(@text,'Add to Bag') or contains(@text,'Add to bag')]")
    ADD_TO_BAG_DESC = (AppiumBy.ACCESSIBILITY_ID, "Add to bag")
    SIZE_POPUP_TITLE = (AppiumBy.XPATH, "//*[contains(@text,'Select Size') or contains(@text,'UK Size')]")
    SIZE_DONE_BUTTON = (AppiumBy.XPATH, "//*[@text='DONE' or contains(@text,'DONE') or contains(@text,'Done')]")
    GO_TO_BAG = (AppiumBy.ID, "com.myntra.android:id/go_to_bag")
    GO_TO_BAG_TEXT = (AppiumBy.XPATH, "//*[contains(@text,'GO TO BAG') or contains(@text,'Go to Bag') or contains(@text,'Go to bag')]")
    GO_TO_BAG_TEXT_LOWER = (AppiumBy.XPATH, "//*[contains(translate(@text,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'go to bag')]")
    GO_TO_BAG_DESC_LOWER = (AppiumBy.XPATH, "//*[contains(translate(@content-desc,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'go to bag')]")
    ADD_TO_BAG_TEXT_LOWER = (AppiumBy.XPATH, "//*[contains(translate(@text,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'add to bag')]")
    ADD_TO_BAG_DESC_LOWER = (AppiumBy.XPATH, "//*[contains(translate(@content-desc,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'add to bag')]")


class BagPageLocators:
    """Locators for shopping bag: items, remove, quantity, Place Order, empty state."""
    CART_ICON = (AppiumBy.ID, "com.myntra.android:id/cart_count")
    CART_ICON_ALT = (AppiumBy.XPATH, "//*[(contains(@content-desc,'Bag') or contains(@content-desc,'Cart')) and not(contains(@content-desc,'Add to')) and not(contains(@text,'Add to'))]")
    BAG_ITEMS = (AppiumBy.ID, "com.myntra.android:id/bag_item")
    FIRST_BAG_ITEM_CARD = (AppiumBy.XPATH, "(//*[contains(@resource-id,'bag_item') or contains(@resource-id,'cart_item') or contains(@resource-id,'product')])[1]")
    REMOVE_ITEM = (AppiumBy.ID, "com.myntra.android:id/remove_item")
    REMOVE_ITEM_XPATH = (AppiumBy.XPATH, "//*[contains(@content-desc,'Remove') or contains(@content-desc,'Delete') or contains(@resource-id,'remove')]")
    ITEM_CLOSE_X = (AppiumBy.XPATH, "//*[contains(@resource-id,'bag_item') or contains(@resource-id,'cart_item')]//*[contains(@content-desc,'Close') or contains(@resource-id,'close') or contains(@content-desc,'Remove') or contains(@content-desc,'Delete')]")
    ITEM_CLOSE_X_FIRST_CARD = (AppiumBy.XPATH, "(//*[contains(@resource-id,'bag_item') or contains(@resource-id,'cart_item')])[1]//*[contains(@content-desc,'Remove') or contains(@content-desc,'Delete') or contains(@content-desc,'Close') or contains(@resource-id,'remove') or contains(@resource-id,'close')]")
    ITEM_CLOSE_X_LAST_IMAGE = (AppiumBy.XPATH, "(//*[contains(@resource-id,'bag_item') or contains(@resource-id,'cart_item')])[1]//android.widget.ImageView[last()]")
    ITEM_CLOSE_X_BY_SIZE_CARD = (AppiumBy.XPATH, "//*[contains(@text,'Size:') or contains(@text,'Qty:')]/ancestor::*[contains(@resource-id,'bag_item') or contains(@resource-id,'item') or contains(@resource-id,'product')][1]//android.widget.ImageView[last()]")
    ITEM_CLOSE_X_LAST_CLICKABLE = (AppiumBy.XPATH, "(//*[contains(@resource-id,'bag_item') or contains(@resource-id,'cart_item')])[1]//*[@clickable='true'][last()]")
    ITEM_CLOSE_X_ALT = (AppiumBy.XPATH, "//*[contains(@text,'ITEMS SELECTED')]/following-sibling::*//*[contains(@content-desc,'Delete') or contains(@content-desc,'Remove') or contains(@resource-id,'remove')]")
    TRASH_DELETE_ICON = (AppiumBy.XPATH, "//*[contains(@content-desc,'Delete') or contains(@content-desc,'Remove') or contains(@content-desc,'Trash')]")
    CONFIRM_REMOVE = (AppiumBy.ID, "android:id/button1")
    CONFIRM_REMOVE_TEXT = (AppiumBy.XPATH, "//*[contains(@text,'Remove') or contains(@text,'REMOVE') or contains(@text,'OK') or contains(@text,'Yes')]")
    POPUP_REMOVE_BUTTON = (AppiumBy.XPATH, "//*[@text='REMOVE' or @text='Remove' or contains(@text,'REMOVE') or contains(@text,'Remove')]")
    POPUP_REMOVE_BY_DESC = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("Remove")')
    POPUP_REMOVE_BY_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("REMOVE")')
    POPUP_REMOVE_BUTTON2 = (AppiumBy.ID, "android:id/button2")
    EMPTY_BAG_MESSAGE = (AppiumBy.XPATH, "//*[contains(@text, 'empty') or contains(@text, 'nothing')]")
    QTY_DROPDOWN = (AppiumBy.XPATH, "//*[contains(@text,'Qty') or contains(@text,'QTY') or contains(@text,'Quantity')]")
    QTY_OPTION_2 = (AppiumBy.XPATH, "//*[@text='2' or contains(@text,'Qty: 2')]")
    QUANTITY_PLUS = (AppiumBy.XPATH, "//*[contains(@content-desc, 'Increase') or contains(@content-desc, 'Add') or @content-desc='+' or contains(@resource-id, 'plus') or contains(@resource-id, 'increment')]")
    QUANTITY_PLUS_TEXT = (AppiumBy.XPATH, "//*[@text='+' or contains(@text,'+')]")
    PROCEED_TO_CHECKOUT = (AppiumBy.XPATH, "//*[contains(@text,'Proceed') or contains(@text,'PROCEED') or contains(@text,'Checkout') or contains(@text,'CHECKOUT') or contains(@text,'Place Order')]")
    PLACE_ORDER_BUTTON = (AppiumBy.XPATH, "//*[contains(@text,'PLACE ORDER') or contains(@text,'Place Order')]")
    PROCEED_BUTTON = (AppiumBy.ID, "com.myntra.android:id/checkout")
    BAG_SCREEN_TITLE = (AppiumBy.XPATH, "//*[contains(@text,'SHOPPING BAG') or contains(@text,'Shopping Bag')]")
    BAG_SCREEN_ITEMS_SELECTED = (AppiumBy.XPATH, "//*[contains(@text,'ITEMS SELECTED') or contains(@text,'Item selected') or contains(@text,'Items selected')]")


class PopupLocators:
    """Locators for onboarding, permission dialogs, login/signup screen, and profile back."""
    TOP_RIGHT_CLOSE_X = (AppiumBy.ACCESSIBILITY_ID, "Close")
    TOP_RIGHT_CLOSE_X_DESC = (AppiumBy.XPATH, "//*[contains(@content-desc, 'Close') or contains(@content-desc, 'close')]")
    TOP_RIGHT_CLOSE_X_ICON = (AppiumBy.XPATH, "//android.widget.ImageView[contains(@content-desc, 'Close') or contains(@content-desc, 'close')]")
    ONBOARDING_CLOSE = (AppiumBy.ID, "com.myntra.android:id/close")
    ALLOW_BUTTON = (AppiumBy.ID, "com.android.packageinstaller:id/permission_allow_button")
    ALLOW_BUTTON_GOOGLE = (AppiumBy.ID, "com.google.android.permissioncontroller:id/permission_allow_button")
    ALLOW_WHILE_USING = (AppiumBy.XPATH, "//*[contains(@text, 'While using the app') or contains(@text, 'Allow') or contains(@text, 'ALLOW')]")
    SKIP_BUTTON = (AppiumBy.ID, "com.myntra.android:id/skip")
    CLOSE_BUTTON = (AppiumBy.ID, "com.myntra.android:id/close")
    MAYBE_LATER = (AppiumBy.XPATH, "//*[contains(@text, 'Maybe Later') or contains(@text, 'Skip')]")
    NOT_NOW = (AppiumBy.XPATH, "//*[contains(@text, 'Not Now')]")
    GET_STARTED = (AppiumBy.XPATH, "//*[contains(@text, 'Get Started') or contains(@text, 'Get started')]")
    NEXT_BUTTON = (AppiumBy.XPATH, "//*[contains(@text, 'Next') or contains(@text, 'NEXT')]")
    CONTINUE_BTN = (AppiumBy.XPATH, "//*[contains(@text, 'Continue') or contains(@text, 'CONTINUE')]")
    LETS_GO = (AppiumBy.XPATH, "//*[contains(@text, \"Let's Go\") or contains(@text, 'Lets Go')]")
    SKIP_TEXT = (AppiumBy.XPATH, "//*[contains(@text, 'Skip') or contains(@text, 'SKIP')]")
    DENY_BUTTON = (AppiumBy.ID, "com.android.packageinstaller:id/permission_deny_button")
    PROFILE_SCREEN_TITLE = (AppiumBy.XPATH, "//*[@text='Profile' or contains(@text, 'Profile')]")
    PROFILE_LOGIN_BUTTON = (AppiumBy.XPATH, "//*[contains(@text, 'LOG IN') or contains(@text, 'SIGN UP')]")
    LOGIN_LOGIN_SIGNUP_TEXT = (AppiumBy.XPATH, "//*[contains(@text,'LOG IN') or contains(@text,'Log in') or contains(@text,'Sign up') or contains(@text,'SIGN UP')]")
    LOGIN_LOGIN_SIGNUP_DESC = (AppiumBy.XPATH, "//*[contains(@content-desc,'LOG IN') or contains(@content-desc,'Log in') or contains(@content-desc,'Sign up') or contains(@content-desc,'SIGN UP')]")
    LOGIN_SIGNIN_TEXT = (AppiumBy.XPATH, "//*[contains(@text,'Login') or contains(@text,'login') or contains(@text,'Sign In')]")
    LOGIN_CONTINUE_PHONE = (AppiumBy.XPATH, "//*[contains(@text,'Continue with') or contains(@text,'Phone') or contains(@text,'Email') or contains(@text,'Use your phone')]")
    LOGIN_MOBILE_HINT = (AppiumBy.XPATH, "//*[contains(@text,'Enter your mobile') or contains(@text,'Mobile number')]")
    PROFILE_BACK_ARROW = (AppiumBy.ACCESSIBILITY_ID, "Back")
    PROFILE_BACK_NAVIGATE_UP = (AppiumBy.ACCESSIBILITY_ID, "Navigate up")
    PROFILE_BACK_XPATH = (AppiumBy.XPATH, "//*[contains(@content-desc, 'Back') or contains(@content-desc, 'Navigate')]")
    PROFILE_BACK_UIAUTOMATOR = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.ImageButton")')
    PROFILE_BACK_DESC = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("Back")')
