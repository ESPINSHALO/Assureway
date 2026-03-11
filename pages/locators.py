"""
Element locators for Myntra app.
UPDATE these after inspecting the app with Appium Inspector.
Use resource-id, accessibility-id, or XPath as needed.
"""
from appium.webdriver.common.appiumby import AppiumBy


class HomePageLocators:
    """Home screen locators."""
    # Bottom navigation – wait for this to confirm home is stable
    HOME_TAB = (AppiumBy.XPATH, "//*[contains(@text, 'Home') and (contains(@content-desc, 'Home') or contains(@resource-id, 'home') or .//*[contains(@text, 'Home')])]")
    HOME_TAB_ALT = (AppiumBy.XPATH, "//*[@text='Home']")
    # Search container (rounded bar below Add Delivery Address) – try ID then XPath
    SEARCH_CONTAINER = (AppiumBy.ID, "com.myntra.android:id/search_widget_text")
    SEARCH_CONTAINER_XPATH = (AppiumBy.XPATH, "//*[contains(@resource-id, 'search') and (contains(@content-desc, 'Search') or .//*[@text])]")
    # Search bar by placeholder text (Jeans, Search, etc.)
    SEARCH_BAR_PLACEHOLDER = (AppiumBy.XPATH, "//*[contains(@text,'Jeans') or contains(@text,'Search') or contains(@content-desc,'Search')]")
    # Indicates we're on home (do NOT tap top-right – that would open Profile)
    HOME_INDICATOR = (AppiumBy.XPATH, "//*[contains(@text, 'Add Delivery Address') or contains(@text, 'Delivery') or contains(@text, 'Earrings') or contains(@text, 'Search for') or contains(@text, 'Jeans')]")
    # Search - Update with actual resource-id from Appium Inspector
    SEARCH_ICON = (AppiumBy.ID, "com.myntra.android:id/search_widget_text")
    # Alternatives if resource-id differs:
    # SEARCH_ICON = (AppiumBy.ACCESSIBILITY_ID, "Search")
    # SEARCH_ICON = (AppiumBy.XPATH, "//android.widget.TextView[@text='Search']")
    
    # Bag icon (bottom navigation)
    BAG_ICON = (AppiumBy.ID, "com.myntra.android:id/cart_count")
    BAG_ICON_ACCESSIBILITY = (AppiumBy.ACCESSIBILITY_ID, "Bag")
    BAG_ICON_XPATH = (AppiumBy.XPATH, "//*[contains(@content-desc,'Bag') or contains(@content-desc,'Cart')]")
    
    # Profile/Account
    PROFILE_ICON = (AppiumBy.ID, "com.myntra.android:id/profile")

    # Search bar – accessibility (for tap_search fallbacks)
    SEARCH_ACCESSIBILITY_ID = (AppiumBy.ACCESSIBILITY_ID, "Search")


class SearchPageLocators:
    """Search screen locators."""
    SEARCH_INPUT = (AppiumBy.ID, "com.myntra.android:id/search_input")
    SEARCH_INPUT_EDIT = (AppiumBy.CLASS_NAME, "android.widget.EditText")
    # XPath by placeholder text (Jeans, Earrings, Search for, etc.)
    SEARCH_INPUT_PLACEHOLDER_JEANS = (AppiumBy.XPATH, "//android.widget.EditText[contains(@text, 'Jeans') or contains(@text, 'Earrings') or contains(@text, 'Search') or contains(@hint, 'Jeans') or contains(@content-desc, 'Search')]")
    SEARCH_INPUT_EDIT_XPATH = (AppiumBy.XPATH, "//android.widget.EditText")
    SEARCH_RESULTS_LIST = (AppiumBy.ID, "com.myntra.android:id/search_results_recycler")
    SEARCH_RESULTS_XPATH = (AppiumBy.XPATH, "//*[contains(@resource-id, 'search') and contains(@resource-id, 'result')]")
    
    # First product in results
    FIRST_PRODUCT = (AppiumBy.XPATH, "//androidx.recyclerview.widget.RecyclerView//android.view.ViewGroup[1]")

    # Listing page (e.g. SHOES category): Gender, Sort and Filter
    GENDER_BUTTON = (AppiumBy.XPATH, "//*[contains(@text,'GENDER') or contains(@text,'Gender')]")
    GENDER_MALE = (AppiumBy.XPATH, "//*[contains(@text,'Male') or contains(@text,'MALE') or @text='Men']")
    SORT_BUTTON = (AppiumBy.XPATH, "//*[contains(@text,'SORT') or contains(@text,'Sort')]")
    SORT_PRICE_HIGH_TO_LOW = (AppiumBy.XPATH, "//*[contains(@text,'Price - high to low') or contains(@text,'Price - High to Low') or contains(@text,'high to low')]")
    SORT_WHATS_NEW = (AppiumBy.XPATH, "//*[contains(@text,\"What's New\") or contains(@text,'Whats New') or contains(@text,'WHAT\'S NEW')]")
    SORT_DISCOUNTS = (AppiumBy.XPATH, "//*[contains(@text,'Discount') or contains(@text,'discount') or contains(@text,'DISCOUNT')]")
    # First GENDER shoe (row 2: model wearing shoes) — skip row 1: [silver shoes | REDTAPE ad]
    # 2-col grid: [1]=silver, [2]=REDTAPE ad, [3]=Top Rated gender shoe, [4]=other gender shoe
    FIRST_GENDER_SHOE_TOP_RATED = (AppiumBy.XPATH, "//*[contains(@text,'Top Rated')]/ancestor::*[@clickable='true'][1]")
    FIRST_PRODUCT_GRID_ITEM = (AppiumBy.XPATH, "(//androidx.recyclerview.widget.RecyclerView)[2]//android.view.ViewGroup[.//android.widget.ImageView][3]")
    FIRST_PRODUCT_GRID_ITEM_ALT = (AppiumBy.XPATH, "(//androidx.recyclerview.widget.RecyclerView)[2]//android.view.ViewGroup[.//android.widget.ImageView][4]")
    FIRST_PRODUCT_GRID_FROM_THIRD = (AppiumBy.XPATH, "(//androidx.recyclerview.widget.RecyclerView)[3]//android.view.ViewGroup[.//android.widget.ImageView][1]")
    FIRST_PRODUCT_CARD = (AppiumBy.XPATH, "(//androidx.recyclerview.widget.RecyclerView)[2]//android.view.ViewGroup[3]")
    FIRST_PRODUCT_CARD_ALT = (AppiumBy.XPATH, "(//androidx.recyclerview.widget.RecyclerView)[2]//android.view.ViewGroup[4]")
    FIRST_SHOE_PRODUCT = (AppiumBy.XPATH, "(//*[contains(@resource-id,'product') or contains(@resource-id,'plp')])[2]")


class ProductPageLocators:
    """Product detail page locators."""
    # Size selector
    SIZE_BUTTON = (AppiumBy.ID, "com.myntra.android:id/select_size")
    SIZE_OPTION = (AppiumBy.XPATH, "//android.widget.TextView[contains(@text, 'UK') or contains(@text, 'US')]")
    # Available sizes: click first available from 5, 6, 7, 8, 9, 10
    SIZE_ANY = (AppiumBy.XPATH, "//*[@text='5' or @text='6' or @text='7' or @text='8' or @text='9' or @text='10' or contains(@text,'UK 5') or contains(@text,'UK 6') or contains(@text,'UK 7') or contains(@text,'UK 8') or contains(@text,'UK 9') or contains(@text,'UK 10') or contains(@text,'US 5') or contains(@text,'US 6') or contains(@text,'US 7') or contains(@text,'US 8') or contains(@text,'US 9') or contains(@text,'US 10')]")
    SELECT_SIZE = (AppiumBy.XPATH, "//*[contains(@text,'Select Size') or contains(@text,'SELECT SIZE')]")

    # Add to bag (multiple fallbacks)
    ADD_TO_BAG = (AppiumBy.ID, "com.myntra.android:id/add_to_bag")
    ADD_TO_BAG_TEXT = (AppiumBy.XPATH, "//*[contains(@text,'ADD TO BAG') or contains(@text,'Add to Bag') or contains(@text,'Add to bag')]")
    ADD_TO_BAG_DESC = (AppiumBy.ACCESSIBILITY_ID, "Add to bag")

    # Select Size pop-up (opens after first Add to bag): available sizes + DONE
    SIZE_POPUP_TITLE = (AppiumBy.XPATH, "//*[contains(@text,'Select Size') or contains(@text,'UK Size')]")
    SIZE_DONE_BUTTON = (AppiumBy.XPATH, "//*[@text='DONE' or contains(@text,'DONE') or contains(@text,'Done')]")

    # Go to bag
    GO_TO_BAG = (AppiumBy.ID, "com.myntra.android:id/go_to_bag")
    GO_TO_BAG_TEXT = (AppiumBy.XPATH, "//*[contains(@text,'GO TO BAG') or contains(@text,'Go to Bag') or contains(@text,'Go to bag')]")
    GO_TO_BAG_TEXT_LOWER = (AppiumBy.XPATH, "//*[contains(translate(@text,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'go to bag')]")
    GO_TO_BAG_DESC_LOWER = (AppiumBy.XPATH, "//*[contains(translate(@content-desc,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'go to bag')]")
    # Add to bag – case-insensitive fallbacks
    ADD_TO_BAG_TEXT_LOWER = (AppiumBy.XPATH, "//*[contains(translate(@text,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'add to bag')]")
    ADD_TO_BAG_DESC_LOWER = (AppiumBy.XPATH, "//*[contains(translate(@content-desc,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'add to bag')]")


class BagPageLocators:
    """Shopping bag page locators."""
    # Cart/Bag icon (top right on product page) — do NOT match "Add to bag" buttons
    CART_ICON = (AppiumBy.ID, "com.myntra.android:id/cart_count")
    # Only header icon: content-desc Bag/Cart but NOT "Add to" (excludes "Add to bag" in product cards)
    CART_ICON_ALT = (AppiumBy.XPATH, "//*[(contains(@content-desc,'Bag') or contains(@content-desc,'Cart')) and not(contains(@content-desc,'Add to')) and not(contains(@text,'Add to'))]")
    BAG_ITEMS = (AppiumBy.ID, "com.myntra.android:id/bag_item")
    # First product card in bag (for tapping X at top-right)
    FIRST_BAG_ITEM_CARD = (AppiumBy.XPATH, "(//*[contains(@resource-id,'bag_item') or contains(@resource-id,'cart_item') or contains(@resource-id,'product')])[1]")
    REMOVE_ITEM = (AppiumBy.ID, "com.myntra.android:id/remove_item")
    REMOVE_ITEM_XPATH = (AppiumBy.XPATH, "//*[contains(@content-desc,'Remove') or contains(@content-desc,'Delete') or contains(@resource-id,'remove')]")
    # X icon on product card (top-right of item) — removes that item (must be inside product card, not header)
    ITEM_CLOSE_X = (AppiumBy.XPATH, "//*[contains(@resource-id,'bag_item') or contains(@resource-id,'cart_item')]//*[contains(@content-desc,'Close') or contains(@resource-id,'close') or contains(@content-desc,'Remove') or contains(@content-desc,'Delete')]")
    # First product card's remove/close icon only (avoid header/toolbar close)
    ITEM_CLOSE_X_FIRST_CARD = (AppiumBy.XPATH, "(//*[contains(@resource-id,'bag_item') or contains(@resource-id,'cart_item')])[1]//*[contains(@content-desc,'Remove') or contains(@content-desc,'Delete') or contains(@content-desc,'Close') or contains(@resource-id,'remove') or contains(@resource-id,'close')]")
    # X is often the last ImageView inside the product card (top-right; card has checkmark, product image, then X)
    ITEM_CLOSE_X_LAST_IMAGE = (AppiumBy.XPATH, "(//*[contains(@resource-id,'bag_item') or contains(@resource-id,'cart_item')])[1]//android.widget.ImageView[last()]")
    # Card containing "Size:" / "Qty:" — then last ImageView in that card (the X)
    ITEM_CLOSE_X_BY_SIZE_CARD = (AppiumBy.XPATH, "//*[contains(@text,'Size:') or contains(@text,'Qty:')]/ancestor::*[contains(@resource-id,'bag_item') or contains(@resource-id,'item') or contains(@resource-id,'product')][1]//android.widget.ImageView[last()]")
    # Small X may be the last clickable node in the first bag item
    ITEM_CLOSE_X_LAST_CLICKABLE = (AppiumBy.XPATH, "(//*[contains(@resource-id,'bag_item') or contains(@resource-id,'cart_item')])[1]//*[@clickable='true'][last()]")
    ITEM_CLOSE_X_ALT = (AppiumBy.XPATH, "//*[contains(@text,'ITEMS SELECTED')]/following-sibling::*//*[contains(@content-desc,'Delete') or contains(@content-desc,'Remove') or contains(@resource-id,'remove')]")
    # Trash/delete icon near "1/1 ITEMS SELECTED"
    TRASH_DELETE_ICON = (AppiumBy.XPATH, "//*[contains(@content-desc,'Delete') or contains(@content-desc,'Remove') or contains(@content-desc,'Trash')]")
    # Confirmation popup after tapping X on card: click "Remove" button
    CONFIRM_REMOVE = (AppiumBy.ID, "android:id/button1")  # OK/Remove confirmation
    CONFIRM_REMOVE_TEXT = (AppiumBy.XPATH, "//*[contains(@text,'Remove') or contains(@text,'REMOVE') or contains(@text,'OK') or contains(@text,'Yes')]")
    POPUP_REMOVE_BUTTON = (AppiumBy.XPATH, "//*[@text='REMOVE' or @text='Remove' or contains(@text,'REMOVE') or contains(@text,'Remove')]")
    POPUP_REMOVE_BY_DESC = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("Remove")')
    POPUP_REMOVE_BY_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("REMOVE")')
    # Two-button dialog: button1 = Cancel (left), button2 = REMOVE (right)
    POPUP_REMOVE_BUTTON2 = (AppiumBy.ID, "android:id/button2")
    EMPTY_BAG_MESSAGE = (AppiumBy.XPATH, "//*[contains(@text, 'empty') or contains(@text, 'nothing')]")
    # Quantity: dropdown on bag page (Qty: 1, then select 2)
    QTY_DROPDOWN = (AppiumBy.XPATH, "//*[contains(@text,'Qty') or contains(@text,'QTY') or contains(@text,'Quantity')]")
    QTY_OPTION_2 = (AppiumBy.XPATH, "//*[@text='2' or contains(@text,'Qty: 2')]")
    # Fallback: plus button if UI uses it
    QUANTITY_PLUS = (AppiumBy.XPATH, "//*[contains(@content-desc, 'Increase') or contains(@content-desc, 'Add') or @content-desc='+' or contains(@resource-id, 'plus') or contains(@resource-id, 'increment')]")
    QUANTITY_PLUS_TEXT = (AppiumBy.XPATH, "//*[@text='+' or contains(@text,'+')]")
    # Proceed to checkout
    PROCEED_TO_CHECKOUT = (AppiumBy.XPATH, "//*[contains(@text,'Proceed') or contains(@text,'PROCEED') or contains(@text,'Checkout') or contains(@text,'CHECKOUT') or contains(@text,'Place Order')]")
    PLACE_ORDER_BUTTON = (AppiumBy.XPATH, "//*[contains(@text,'PLACE ORDER') or contains(@text,'Place Order')]")
    PROCEED_BUTTON = (AppiumBy.ID, "com.myntra.android:id/checkout")  # if exists
    # Shopping Bag screen detection (any of these = we're on bag page)
    BAG_SCREEN_TITLE = (AppiumBy.XPATH, "//*[contains(@text,'SHOPPING BAG') or contains(@text,'Shopping Bag')]")
    BAG_SCREEN_ITEMS_SELECTED = (AppiumBy.XPATH, "//*[contains(@text,'ITEMS SELECTED') or contains(@text,'Item selected') or contains(@text,'Items selected')]")


class PopupLocators:
    """Common popup/dialog locators (onboarding, login prompts)."""
    # Onboarding "Your Favorite Brands" screen - top-right X to go to home
    TOP_RIGHT_CLOSE_X = (AppiumBy.ACCESSIBILITY_ID, "Close")
    TOP_RIGHT_CLOSE_X_DESC = (AppiumBy.XPATH, "//*[contains(@content-desc, 'Close') or contains(@content-desc, 'close')]")
    TOP_RIGHT_CLOSE_X_ICON = (AppiumBy.XPATH, "//android.widget.ImageView[contains(@content-desc, 'Close') or contains(@content-desc, 'close')]")
    # Myntra onboarding close (resource-id - update in Appium Inspector if needed)
    ONBOARDING_CLOSE = (AppiumBy.ID, "com.myntra.android:id/close")

    # Android permission dialog - Allow/While using app (varies by Android version)
    ALLOW_BUTTON = (AppiumBy.ID, "com.android.packageinstaller:id/permission_allow_button")
    ALLOW_BUTTON_GOOGLE = (AppiumBy.ID, "com.google.android.permissioncontroller:id/permission_allow_button")
    ALLOW_WHILE_USING = (AppiumBy.XPATH, "//*[contains(@text, 'While using the app') or contains(@text, 'Allow') or contains(@text, 'ALLOW')]")
    
    SKIP_BUTTON = (AppiumBy.ID, "com.myntra.android:id/skip")
    # SKIP_BUTTON = (AppiumBy.XPATH, "//*[contains(@text, 'Skip')]")
    # SKIP_BUTTON = (AppiumBy.XPATH, "//*[contains(@text, 'Later')]")
    
    CLOSE_BUTTON = (AppiumBy.ID, "com.myntra.android:id/close")
    
    # Login popup dismiss
    MAYBE_LATER = (AppiumBy.XPATH, "//*[contains(@text, 'Maybe Later') or contains(@text, 'Skip')]")
    NOT_NOW = (AppiumBy.XPATH, "//*[contains(@text, 'Not Now')]")

    # Onboarding / running screens - tap to move past
    GET_STARTED = (AppiumBy.XPATH, "//*[contains(@text, 'Get Started') or contains(@text, 'Get started')]")
    NEXT_BUTTON = (AppiumBy.XPATH, "//*[contains(@text, 'Next') or contains(@text, 'NEXT')]")
    CONTINUE_BTN = (AppiumBy.XPATH, "//*[contains(@text, 'Continue') or contains(@text, 'CONTINUE')]")
    LETS_GO = (AppiumBy.XPATH, "//*[contains(@text, \"Let's Go\") or contains(@text, 'Lets Go')]")
    SKIP_TEXT = (AppiumBy.XPATH, "//*[contains(@text, 'Skip') or contains(@text, 'SKIP')]")
    DENY_BUTTON = (AppiumBy.ID, "com.android.packageinstaller:id/permission_deny_button")

    # Profile screen (opens ~2 sec after home) – back arrow at top-left to close
    PROFILE_SCREEN_TITLE = (AppiumBy.XPATH, "//*[@text='Profile' or contains(@text, 'Profile')]")
    PROFILE_LOGIN_BUTTON = (AppiumBy.XPATH, "//*[contains(@text, 'LOG IN') or contains(@text, 'SIGN UP')]")
    # Login screen indicators (after Place Order)
    LOGIN_LOGIN_SIGNUP_TEXT = (AppiumBy.XPATH, "//*[contains(@text,'LOG IN') or contains(@text,'Log in') or contains(@text,'Sign up') or contains(@text,'SIGN UP')]")
    LOGIN_LOGIN_SIGNUP_DESC = (AppiumBy.XPATH, "//*[contains(@content-desc,'LOG IN') or contains(@content-desc,'Log in') or contains(@content-desc,'Sign up') or contains(@content-desc,'SIGN UP')]")
    LOGIN_SIGNIN_TEXT = (AppiumBy.XPATH, "//*[contains(@text,'Login') or contains(@text,'login') or contains(@text,'Sign In')]")
    LOGIN_CONTINUE_PHONE = (AppiumBy.XPATH, "//*[contains(@text,'Continue with') or contains(@text,'Phone') or contains(@text,'Email') or contains(@text,'Use your phone')]")
    LOGIN_MOBILE_HINT = (AppiumBy.XPATH, "//*[contains(@text,'Enter your mobile') or contains(@text,'Mobile number')]")
    PROFILE_BACK_ARROW = (AppiumBy.ACCESSIBILITY_ID, "Back")
    PROFILE_BACK_NAVIGATE_UP = (AppiumBy.ACCESSIBILITY_ID, "Navigate up")
    PROFILE_BACK_XPATH = (AppiumBy.XPATH, "//*[contains(@content-desc, 'Back') or contains(@content-desc, 'Navigate')]")
    # UiAutomator – toolbar back/ImageButton (often used for back)
    PROFILE_BACK_UIAUTOMATOR = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.ImageButton")')
    PROFILE_BACK_DESC = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("Back")')
