# Mobile App Automation Testing for Myntra

Appium + Python automation framework for testing the Myntra Android application on an emulator.

## Project goals

- Launch the Myntra app and reach the home screen (dismiss onboarding with Back).
- Search for products (e.g. shoes), apply filters and sort, open a product and add it to the bag.
- Change quantity in the bag, proceed to Place Order, handle the login prompt if it appears, then empty the cart and return to home.
- Use explicit waits, clear logging, and reusable helpers (no coordinate hacks where avoidable).

## Main automation flow (end-to-end script)

The script **`scripts/open_myntra_home.py`** runs a full user journey in human terms:

1. **Launch** – Start the Myntra app and create the Appium session.

2. **Reach home** – Wait for the first screen (splash/onboarding) to show, then press Back once so the app goes to the home screen instead of exiting. No extra Back presses so the app does not close.

3. **Search** – Go to the search bar, type **shoes**, and submit. If the profile screen opens in between, it presses Back once and continues. Search uses short timeouts and several locators so the bar is found quickly.

4. **Results and filters** – On the shoes listing, it selects **Gender → Male**, opens **Sort**, chooses **Discounts**, then opens the **first shoe** in the list (tap in the product area so it does not hit banners or filters).

5. **Product and add to bag** – On the product page it taps **Add to bag**. When the size pop-up appears it picks the first available size from 5–10 and taps **DONE**.

6. **Bag and quantity** – It goes back to home, opens the **bag** from the bottom navigation, sets **quantity to 2** via the quantity dropdown and confirms with **DONE**, then taps **Place Order**.

7. **Login prompt** – If a login screen appears after Place Order, the script closes it (X or top-right tap) and returns to the home screen.

8. **Empty cart** – It opens the bag again. On the Shopping Bag screen it finds the product card (using “Qty” or “Size” to know where the card is) and taps the **X** at the top-right of that card. When the confirmation popup appears (**Cancel** and **REMOVE**), it taps **REMOVE** (by finding the button or by tapping the right side of the dialog where REMOVE usually is). Then it presses Back until the Home tab is visible.

9. **Finish** – The app stays open for 15 seconds (or until you press Ctrl+C if you use `--stay`), then the driver quits.

All of this is done with **explicit waits** and **element-based** actions where possible. A small helper is used for taps that must be by position (e.g. the card X and the REMOVE button), using Appium’s mobile gesture or W3C actions so taps register reliably.

## How to run the main script

From the project root with the virtual environment activated:

```bash
# Full flow, then app stays open 15 seconds and closes
python scripts/open_myntra_home.py

# Keep the app open until you press Ctrl+C
python scripts/open_myntra_home.py --stay

# Skip selecting Gender = Male on the shoes page
python scripts/open_myntra_home.py --no-male
```

**Before running:** Start the Appium server (`appium`) and have the Android emulator running with the Myntra app installed.

## Project structure

```
Assureway/
├── config/
│   ├── capabilities.py      # Appium capabilities (app package, activity)
│   └── __init__.py
├── core/
│   ├── driver_factory.py     # Appium WebDriver creation (implicit wait 0)
│   └── __init__.py
├── pages/
│   ├── locators.py           # Element locators (search, bag, product, popup)
│   ├── base_page.py
│   ├── home_page.py
│   ├── search_page.py
│   ├── product_page.py
│   ├── bag_page.py
│   ├── popup_handler.py
│   └── __init__.py
├── scripts/
│   └── open_myntra_home.py   # Full flow: launch → search → bag → empty cart → home
├── tests/
│   ├── test_app_launch.py
│   ├── test_home_screen.py
│   ├── test_search_flow.py
│   ├── test_add_to_bag.py
│   ├── test_bag_operations.py
│   └── test_navigation.py
├── utils/
│   ├── logger.py
│   ├── waits.py
│   └── __init__.py
├── reports/                  # Logs (e.g. automation_YYYYMMDD.log)
├── conftest.py
├── pytest.ini
├── requirements.txt
└── README.md
```

## Prerequisites

1. **Python 3.10+** and a virtual environment.
2. **Android Studio** – SDK and emulator.
3. **Appium** – e.g. `npm install -g appium`.
4. **UiAutomator2** – `appium driver install uiautomator2`.
5. **ADB** – from Android SDK.
6. **Myntra app** – installed on the emulator (Play Store or APK).

## Setup

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
# or: venv\Scripts\activate   # Windows

pip install -r requirements.txt
```

Start the emulator, install Myntra, then start Appium: `appium`.

## Configuration

- **App package and activity** – Set in `config/capabilities.py`. To see the current activity when Myntra is open:  
  `adb shell dumpsys window | grep -E 'mCurrentFocus'`
- **Locators** – Adjust `pages/locators.py` after inspecting the app in Appium Inspector (search bar, bag icon, product card X, REMOVE button, etc.).

## Running tests (pytest)

```bash
pytest
pytest --html=reports/report.html --self-contained-html
pytest tests/test_app_launch.py -v
pytest -v -s
```

## Test scenarios covered

| Test            | Description                          |
|-----------------|--------------------------------------|
| App launch      | App starts and home loads            |
| Onboarding      | Login/skip dialogs handled           |
| Home screen     | Search icon and navigation           |
| Search flow     | Tap search, enter "shoes", results   |
| Product details | Open product, details page          |
| Add to bag      | Select size, add item, bag          |
| Bag operations  | Remove item, quantity, checkout     |
| Navigation      | Scroll, transitions, popups         |

## Notes

- **Locators** – Myntra may use custom IDs; update `pages/locators.py` with Appium Inspector.
- **Emulator** – Fully boot before running the script or tests.
- **Appium** – Must be running before execution.
- **Logs** – Written under `reports/` (e.g. `automation_YYYYMMDD.log`).

## Tools and technologies

- **Appium** – Mobile automation
- **UiAutomator2** – Android driver
- **Python** – Script and tests
- **pytest** – Test runner
- **Appium Python Client** – Appium bindings
