# Mobile App Automation Testing for Myntra

Appium and Python automation framework for testing the Myntra Android app on an emulator. The project includes a standalone automation script for a full user journey and a pytest test suite with clear test order, failure screenshots, and HTML reports.

## What this project does

- **Launches** the Myntra app and handles the first screen (splash or onboarding) with a single Back press so the app reaches home instead of closing.
- **Searches** for products (e.g. shoes), applies Gender and Sort filters, opens a product, selects size, and adds it to the bag.
- **Covers bag and checkout**: opens the bag from home, changes quantity, taps Place Order, handles the login screen (closes it and returns), then removes the item and returns to home.
- Uses **explicit waits**, **reusable helpers**, and **element-based** actions where possible, with position-based taps only where the UI requires it.

## Tech Stack

* Python – Automation scripting
* Appium – Mobile automation framework
* UiAutomator2 – Android driver for Appium
* Pytest – Test runner and framework
* pytest-html – HTML report generation
* Android Emulator – Test execution environment
* ADB – Android device communication

---

## Quick start

**Prerequisites:** Python 3.10+, Android emulator with Myntra installed, Appium server and UiAutomator2 driver, ADB.

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux  |  venv\Scripts\activate on Windows
pip install -r requirements.txt
```

Start the emulator and run Appium (`appium`) before executing the script or tests.

---

## Run the automation script (full flow, no pytest)

From the project root with the virtual environment active:

```bash
# Full flow, then app closes after a short delay
python scripts/open_myntra_home.py

# Keep the app open until you press Ctrl+C
python scripts/open_myntra_home.py --stay

# Skip selecting Gender = Male on the shoes listing
python scripts/open_myntra_home.py --no-male
```

The script runs: launch → reach home → search “shoes” → Gender Male, Sort Discounts → open first product → add to bag (size + DONE) → home → open bag → quantity 2 → Place Order → close login if shown → open bag again → remove item → empty cart → return home.

---

## Run the test suite (pytest)

Tests run in a fixed order so the flow makes sense. Each test gets a new driver session.

```bash
# Run all tests
pytest tests/ -v

# Run all tests and generate an HTML report
pytest tests/ -v --html=reports/report.html --self-contained-html

# Run a single test file
pytest tests/test_app_launch.py -v

# Run a single test
pytest tests/test_search_flow.py::test_sort_select_discounts -v
```

**On failure:** A screenshot is saved under `reports/screenshots/` with a name like `test_name_YYYYMMDD_HHMMSS.png`. The path is printed in the terminal.

---

## Test structure and order

Tests are ordered by design: app launch → home → search flow → cart and checkout → full end-to-end.

| Order | File | What it covers |
|-------|------|-----------------|
| 1 | **test_app_launch.py** | (1) App opens and is closed immediately. (2) App opens, Back is pressed to dismiss the popup, then the app is closed (no wait for home). |
| 2 | **test_home_screen.py** | (1) Home screen loads (search bar or Home tab visible). (2) Search icon is tappable and opens search. |
| 3 | **test_search_flow.py** | Search “shoes”, then in order: listing visible → Gender Male → Sort Discounts → open first product → select size and add to bag. |
| 4 | **test_cart_checkout_flow.py** | After add-to-bag setup: navigate to home → open cart, set quantity to 2, DONE → click Place Order and confirm login screen → back from login → remove product from cart → verify empty cart and return home. |
| 5 | **test_full_e2e_flow.py** | Single test that runs the full journey in one go (popups → search → filters → add to bag → cart → Place Order → back from login → remove → home). |

**Total:** 16 test cases across 5 files. The first three tests focus only on launch, popup handling, and home; the rest cover search, product, bag, and checkout.

---

## Reports and screenshots

- **HTML report** – Generate with:  
  `pytest tests/ -v --html=reports/report.html --self-contained-html`  
  Open `reports/report.html` in a browser.

- **Failure screenshots** – When a test fails, a screenshot is written to **reports/screenshots/** and the path is printed (e.g. `[pytest] Screenshot saved: .../reports/screenshots/test_xxx_20260308_125657.png`).

- **Logs** – Automation logs (e.g. `reports/automation_YYYYMMDD.log`) are generated when the script or tests run; `*.log` is in `.gitignore`. The `reports/` folder may contain `report.html` and `reports/screenshots/`; these can be committed if you want to share them.

## Test Execution Result

All automated test cases executed successfully.

Example terminal output:

16 passed in ~23 minutes

The test suite includes:

* Smoke tests
* Functional tests
* Cart and checkout validation
* Full end-to-end user journey

## Framework Architecture

Test Cases (pytest)
↓
Page Object Model
↓
Reusable Utilities (waits, logger)
↓
Appium Driver
↓
Android Emulator (Myntra App)

---

## Project structure

```
Assureway/
├── config/              # Appium capabilities (app package, activity)
├── core/                # Driver creation and teardown
├── pages/               # Page objects and locators (home, search, product, bag, popup)
├── scripts/
│   └── open_myntra_home.py   # Standalone automation: full flow from launch to empty cart
├── tests/
│   ├── test_app_launch.py    # App launch and popup handling
│   ├── test_home_screen.py   # Home load and search icon
│   ├── test_search_flow.py  # Search, filters, product, add to bag
│   ├── test_cart_checkout_flow.py  # Cart, quantity, Place Order, login, remove, empty
│   └── test_full_e2e_flow.py # Single full end-to-end test
├── utils/               # Logger, waits, helpers
├── reports/             # report.html, screenshots/, logs (optional)
├── conftest.py          # Pytest fixtures, test order, screenshot-on-failure hook
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## Configuration

- **App package and activity** – In `config/capabilities.py`. To see the current activity:  
  `adb shell dumpsys window | grep -E 'mCurrentFocus'`
- **Locators** – In `pages/locators.py`. Update after inspecting the app in Appium Inspector (search bar, bag icon, product card, REMOVE button, etc.).

---

## Design choices

- **Test order** – Defined in `conftest.py` (`TEST_FILE_ORDER` and `TEST_ORDER_IN_FILE`) so pytest runs tests in a logical flow.
- **No skips for setup** – If a step (e.g. add to bag) fails, the test fails with a clear assertion instead of being skipped, so you see real failures and get a screenshot.
- **Retries for add-to-bag setup** – Cart and checkout tests retry the add-to-bag setup (search → gender → sort → open product → add to bag) up to twice to reduce flakiness when the emulator is slow.
- **First three tests** – Test 1 only checks that the app opens and then closes it. Test 2 opens the app, presses Back once to dismiss the popup, then closes the app. Test 3 uses the full “app launched” fixture and asserts that the home screen is visible.

---

## Tools and technologies

- **Appium** – Mobile automation
- **UiAutomator2** – Android driver for Appium
- **Python** – Automation and tests
- **pytest** – Test runner, with pytest-html for reports
- **Appium Python Client** – Appium bindings for Python

---

## Notes

- Ensure the emulator is fully booted and the Myntra app is installed before running.
- Start the Appium server before executing the script or tests.
- If the app UI changes, update `pages/locators.py` using Appium Inspector.
