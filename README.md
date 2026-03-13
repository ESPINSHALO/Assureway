## Myntra Android Automation Framework (Appium + Python)

End-to-end mobile test automation framework for the Myntra Android application, built with Appium, Python and Pytest. It demonstrates production-style design, Page Object Model, explicit waits, and robust handling of real-world UI flakiness.

---

## Overview

This project automates core user journeys on the Myntra Android app running in an emulator:

- Launching the app and handling onboarding / permission popups
- Reaching the home screen reliably
- Searching for products (e.g. shoes)
- Applying listing filters (Gender, Sort)
- Opening product details and adding items to the shopping bag
- Cart and checkout interactions (quantity changes, Place Order, login screen handling)
- Full end-to-end flows that cover search → product → bag → checkout → back from login → remove item → home

The framework is designed as a teaching-quality example of how to structure a mobile automation project for a real QA team: clean separation of concerns, centralized configuration, reusable flows, and clear reporting.

---

## Demo Video

A recorded run of the full automation flow  
(launch → search → filters → product → add to bag → return home → open cart and increase quantity → Place Order → back from login to home → reopen cart → remove item → return home)  
is available here:  
[**Myntra Automation Framework – end-to-end flow**](https://drive.google.com/file/d/1ctDRyueELu1KiYrkCn2oTJiloiTShNNt/view?usp=sharing).

---

## Tech Stack

- **Language**: Python
- **Automation**: Appium
- **Driver**: UiAutomator2 (Android)
- **Test framework**: Pytest
- **Reports**: `pytest-html` (HTML reports)
- **Device**: Android Emulator (AVD)
- **Bindings**: Appium Python Client
- **Utilities**: ADB for screenshot fallback when the driver is dead

Dependencies are listed in `requirements.txt`.

---

## AI Assistance

AI-assisted development tools were used during the development of this project to improve productivity and accelerate certain development tasks.

- **Cursor AI** was used for code suggestions, refactoring assistance, and limited code generation while building the framework.
- **ChatGPT 5.2** was used for learning about the Myntra application, the tech stack (Appium, Pytest, etc.), and understanding how the code and automation flow work.

The overall framework architecture, Page Object Model design, test scenarios, and execution strategy were designed and validated manually. AI was treated as a helper to speed up routine coding and learning, not as a replacement for design or review. This matches how many modern engineering teams use AI tooling in their day-to-day work.

---

## Framework Architecture

The framework follows a Page Object Model (POM) and layered design:

- **Page Object Model (POM)**  
  Each screen of the Myntra app has its own page class under `pages/`:
  - `HomePage` – home screen, search bar, bag icon
  - `SearchPage` – search input, results, listing filters
  - `ProductPage` – product details, sizes, Add to bag, Go to bag
  - `BagPage` – shopping bag/cart, quantity, Place Order, empty state
  - `PopupHandler` – onboarding, permissions, profile, login dialogs

  All page classes inherit from `BasePage`, which centralizes common actions and wait helpers.

- **Locator encapsulation**  
  All Appium locators are defined in `pages/locators.py`, grouped by page.  
  Tests never contain locators directly; they use page methods and helper flows.

- **Core and configuration separation**
  - `config/capabilities.py` defines all Appium capabilities and app constants (package, activity, device, platform) in one place.
  - `core/driver_factory.py` creates and tears down the Appium `WebDriver`, using the centralized capabilities.

- **Reusable utilities**
  - `utils/logger.py` defines a single logger used across the framework, writing to both console and a daily log file under `reports/`.
  - `utils/waits.py` houses explicit wait helpers (`wait_for_element`, `safe_click`, `element_exists`, etc.) so page classes do not duplicate wait logic.

- **Test orchestration and hooks**
  - `conftest.py` provides:
    - driver fixture (one fresh driver per test)
    - `app_launched` fixture that brings the app to the home screen (handles popups, then waits for home)
    - centralized test order (launch → home → search → cart/checkout → full E2E)
    - a pytest hook that captures screenshots on failure (with ADB fallback when the driver session is dead)

- **Shared flow helpers**
  - `scripts/open_myntra_home.py` defines multi-step flows (search, filters, open product, add to bag, cart operations) used by both:
    - the standalone script entry point
    - tests in `tests/test_search_flow.py` and `tests/test_cart_checkout_flow.py`

---

## Project Structure

```text
Assureway/
├── config/
│   ├── __init__.py              # Export configuration helpers
│   └── capabilities.py          # Appium UiAutomator2 capabilities and app constants
├── core/
│   ├── __init__.py              # Export driver factory functions
│   └── driver_factory.py        # create_driver / quit_driver and Appium server URL
├── pages/
│   ├── __init__.py              # Export page objects
│   ├── base_page.py             # BasePage: shared actions (tap, scroll, back, etc.)
│   ├── locators.py              # All Appium locators (Home, Search, Product, Bag, Popup)
│   ├── home_page.py             # HomePage: search bar, bag icon, home checks
│   ├── search_page.py           # SearchPage: search input, listing filters, first product
│   ├── product_page.py          # ProductPage: size selection, Add to bag, Go to bag
│   ├── bag_page.py              # BagPage: cart contents, quantity, Place Order, empty state
│   └── popup_handler.py         # PopupHandler: onboarding, permissions, login, profile
├── scripts/
│   └── open_myntra_home.py      # Standalone script + shared end-to-end flow helpers
├── tests/
│   ├── __init__.py
│   ├── test_app_launch.py       # App launch and initial popup handling
│   ├── test_home_screen.py      # Home screen loading and search tap
│   ├── test_search_flow.py      # Search, filters, open product, add to bag
│   ├── test_cart_checkout_flow.py  # Cart, Place Order, login, remove, empty cart
│   └── test_full_e2e_flow.py    # Single full end-to-end test in one session
├── utils/
│   ├── __init__.py              # Export logger and wait helpers
│   ├── logger.py                # Central logger (console + file under reports/)
│   └── waits.py                 # Explicit wait and safe-click utilities
├── reports/
│   ├── report.html              # HTML test report (generated by pytest-html)
│   └── screenshots/             # Screenshots captured on test failures (ignored by git)
├── docs/
│   ├── README.md                # Description of sample outputs and assets
│   ├── all-tests-output.png     # Full-suite terminal output
│   ├── regression-tests-output.png  # Regression run terminal output
│   ├── smoke-tests-output.png   # Smoke run terminal output
│   ├── html-tests-output.png    # HTML report generation example
│   ├── myntra-automation-output.png # Standalone automation run output
│   └── failure-test-output.png  # Failure screenshot from a test run
├── conftest.py                  # Pytest configuration, fixtures, hooks, and test ordering
├── pytest.ini                   # Pytest settings and markers (smoke, regression)
├── requirements.txt             # Python dependencies
└── README.md                    # Project documentation
```

---

## Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/ESPINSHALO/Assureway.git
cd Assureway
```

2. **Create and activate a virtual environment**

```bash
python -m venv venv
source venv/bin/activate          # macOS / Linux
# venv\Scripts\activate           # Windows PowerShell / cmd
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Prepare the Android emulator**

- Start an Android emulator (AVD) from Android Studio.
- Ensure the Myntra Android app is installed on the emulator (via Play Store or APK).

Basic checks:

```bash
adb devices
adb shell pm list packages | grep myntra
```

5. **Start the Appium server**

In a separate terminal:

```bash
appium
```

Make sure it is listening on `http://127.0.0.1:4723` (the default in `core/driver_factory.py`).

---

## Running the Automation

### Run the full test suite

```bash
pytest tests/ -v
```

### Run the full test suite with HTML report

```bash
pytest tests/ -v --html=reports/report.html --self-contained-html
```

### Run a specific test file or test

```bash
# Single file
pytest tests/test_search_flow.py -v

# Single test
pytest tests/test_search_flow.py::test_select_size_and_add_to_bag -v
```

### Run the standalone full-flow script (without pytest)

```bash
# Full flow, app closes shortly after finishing
python scripts/open_myntra_home.py

# Keep the app open at the end until you press Ctrl+C
python scripts/open_myntra_home.py --stay

# Run the flow without selecting Gender = Male (if desired)
python scripts/open_myntra_home.py --no-male
```

## Automated Test Scenarios

The test suite covers the following core scenarios:

- **Application launch**
  - `test_app_launches_successfully` – verifies that the Myntra app launches successfully.
  - `test_handle_onboarding_popup` – launches the app, presses Back once to dismiss the first popup.

- **Home screen**
  - `test_home_screen_loads` – checks that the home screen loads and shows key UI (search bar / home tab).
  - `test_tap_search_icon` – verifies that the search icon is tappable and opens the search interface.

- **Search and product selection**
  - `test_search_for_product` – performs a search (e.g. “shoes”) and asserts that the listing page is visible.
  - `test_gender_select_male` – applies the Gender filter and selects “Male”.
  - `test_sort_select_discounts` – opens Sort and selects the “Discounts” option.
  - `test_open_first_product` – opens the first product from the filtered listing and validates the product page.
  - `test_select_size_and_add_to_bag` – selects an available size and adds the product to the bag.

- **Cart and checkout**
  - `test_navigate_to_home_after_add_to_bag` – after add-to-bag, navigates back to home and asserts home is visible.
  - `test_open_cart_increase_quantity_done` – opens the cart, sets quantity to 2, and confirms DONE.
  - `test_click_place_order_opens_login` – clicks Place Order and validates that the login screen appears.
  - `test_back_from_login_to_home` – closes the login screen and returns to the home page.
  - `test_remove_product_from_cart` – opens the cart, removes the product, and checks that the cart is empty.
  - `test_verify_empty_cart_and_return_home` – ensures the cart is empty and the app returns to the home screen.

- **End-to-end flow**
  - `test_full_e2e_flow` – executes the complete user journey in a single test:
    - Popup handling
    - Search and filters
    - Open product and add to bag
    - Cart, quantity update, Place Order
    - Back from login, remove item, final return to home

---

## Framework Features

- **Page Object Model (POM)**
  - Each screen (home, search, product, bag, popups) has its own page class.
  - All locators are centralized in `pages/locators.py`.
  - Tests call page methods and script helpers, not raw locators.

- **Centralized configuration**
  - Appium capabilities are built in `config/capabilities.py`:
    - platform name
    - device name
    - Myntra `APP_PACKAGE` and `APP_ACTIVITY`
    - UiAutomator2-specific options (e.g. server launch timeout)
  - Configuration is reusable and not duplicated in tests.

- **Reusable driver management**
  - `core/driver_factory.py` exposes:
    - `create_driver()` – creates a `WebDriver` with the configured capabilities.
    - `quit_driver()` – closes the driver gracefully.
  - `conftest.py` creates one driver per test via the `driver` fixture, with a short delay after quit to avoid session overlap issues.

- **Explicit waits and robust interactions**
  - `utils/waits.py` provides:
    - `wait_for_element`, `wait_for_element_clickable`, `wait_for_element_visible`
    - `element_exists` and `safe_click`
  - Page methods and flows use explicit waits and selective polling to minimize flaky behavior.
  - Coordinate-based taps are only used as controlled fallbacks when locators cannot be relied on.

- **Logging**
  - Framework-wide logger in `utils/logger.py`:
    - Logs to console and to a daily file under `reports/` (e.g. `automation_YYYYMMDD.log`).
    - Used across driver creation, page methods, and scripts to trace each step.

- **Screenshot on failure**
  - `conftest.py` implements `pytest_runtest_makereport`:
    - On any test failure, attempts `driver.save_screenshot(...)` into `reports/screenshots/`.
    - If the driver session is dead (e.g. instrumentation crash), falls back to:
      ```bash
      adb exec-out screencap -p
      ```
      and still saves the screenshot to `reports/screenshots/`.
    - The screenshot path is written into stderr for quick access.

- **HTML reporting**
  - `pytest-html` is configured via command-line options:
    - `--html=reports/report.html --self-contained-html`
  - The generated HTML report is self-contained and can be opened directly in a browser.

- **Test ordering and fixtures**
  - `conftest.py` defines a deterministic test order via `pytest_collection_modifyitems`, so flows build logically.
  - Fixtures provide ready-to-use page objects (`home_page`, `search_page`, `product_page`, `bag_page`, `popup_handler`) and the `app_launched` state.

---

## Test Reporting

- **HTML reports**

  Generate an HTML report with:

  ```bash
  pytest tests/ -v --html=reports/report.html --self-contained-html
  ```

  - The report file is written to `reports/report.html`.
  - Open it in a browser (macOS example):

  ```bash
  open reports/report.html
  ```

- **Screenshots**

  - On every test failure, a screenshot is saved under:

    ```text
    reports/screenshots/
    ```

  - The filename includes the test name and a timestamp.
  - If the WebDriver cannot capture the screenshot, ADB fallback is used so a screenshot is still produced.
  - A failure screenshot from a test run is kept in `docs/failure-test-output.png` for reference.

- **Logs**

  - Text logs are written to `reports/automation_YYYYMMDD.log` by the central logger.
  - Combined with screenshots and the HTML report, this gives a complete picture of each test run.

---

## Notes

- **Environment requirements**
  - Python 3.10+ is recommended.
  - Android emulator (AVD) must be running before executing tests or scripts.
  - The Myntra Android app must be installed on the emulator.
  - Appium server must be running and reachable at `http://127.0.0.1:4723`.

- **ADB availability**
  - `adb` must be available on the system `PATH` for:
    - basic device checks
    - fallback screenshot capture when the driver is dead.

- **Flakiness and timing**
  - The framework uses explicit waits, defensive checks, and shared flows to reduce flakiness.
  - Some scenarios still depend on real network and UI responsiveness; occasional retries or re-runs may be expected, as in real-world mobile automation.

This repository is intended to demonstrate a complete, maintainable Appium + Python + Pytest framework for a real Android application, with POM, centralized configuration, reusable flows, logging, screenshots, and clean project organization.
