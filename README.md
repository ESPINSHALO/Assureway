# Mobile App Automation Testing for Myntra

Appium + Python automation framework for testing the Myntra Android application on an emulator.

## 🎯 Project Goals

- Launch the Myntra app and handle onboarding/login popups
- Perform product search (e.g., shoes)
- Open product details and add items to bag
- Validate bag operations and navigation
- Modular, reusable automation with explicit waits and logging

## 📁 Project Structure

```
Assureway/
├── config/
│   ├── capabilities.py      # Appium capabilities (app package, activity)
│   └── __init__.py
├── core/
│   ├── driver_factory.py     # Appium WebDriver creation
│   └── __init__.py
├── pages/
│   ├── locators.py           # Element locators (update with Appium Inspector)
│   ├── base_page.py          # Base page object
│   ├── home_page.py
│   ├── search_page.py
│   ├── product_page.py
│   ├── bag_page.py
│   ├── popup_handler.py
│   └── __init__.py
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
├── reports/                  # Logs and test reports (auto-created)
├── conftest.py               # Pytest fixtures
├── pytest.ini
├── requirements.txt
└── README.md
```

## ⚙️ Prerequisites

1. **Python 3.10+** with venv
2. **Android Studio** – with SDK and emulator
3. **Appium** – `npm install -g appium`
4. **UiAutomator2 driver** – `appium driver install uiautomator2`
5. **ADB** – Android Debug Bridge (comes with Android SDK)
6. **Myntra app** – Install on emulator via Play Store or APK

## 🚀 Setup

```bash
# 1. Create and activate virtual environment (if not done)
python -m venv venv
source venv/bin/activate   # macOS/Linux
# or: venv\Scripts\activate   # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start Android emulator from Android Studio

# 4. Install Myntra on emulator (Play Store or sideload APK)

# 5. Start Appium server
appium
```

## 🔧 Configuration

### 1. App Package & Activity

Edit `config/capabilities.py` with the correct Myntra app package and launch activity:

```bash
# Find current activity when Myntra is open:
adb shell dumpsys window | grep -E 'mCurrentFocus'
```

Example output: `com.myntra.android/com.myntra.android.activities.HomeActivity`

### 2. Element Locators

Update `pages/locators.py` after inspecting the app with **Appium Inspector**:

- Connect Appium Inspector to `http://127.0.0.1:4723`
- Use your emulator as the target device
- Capture `resource-id`, `content-desc`, or XPath for:
  - Search icon, search input
  - Product cards, Add to Bag, Size selector
  - Bag icon, remove item, etc.

## ▶️ Running Tests

```bash
# Run all tests
pytest

# Run with HTML report
pytest --html=reports/report.html --self-contained-html

# Run smoke tests only
pytest -m smoke

# Run specific test file
pytest tests/test_app_launch.py -v

# Run with more output
pytest -v -s
```

## 🧪 Test Scenarios Covered

| Test | Description |
|------|-------------|
| App launch | Verify app starts and home loads |
| Onboarding popup | Handle login/skip dialogs |
| Home screen | Verify search icon, navigation |
| Search flow | Tap search, enter "shoes", validate results |
| Product details | Open product, verify details page |
| Add to bag | Select size, add item, verify in bag |
| Bag operations | Remove item, navigate back |
| Navigation | Scroll, transitions, popup handling |

## 📝 Notes

- **First run**: Update locators in `pages/locators.py` using Appium Inspector – Myntra may use custom IDs.
- **Emulator**: Ensure emulator is fully booted before starting tests.
- **Appium**: Must be running before test execution (`appium`).
- **Logs**: Stored in `reports/automation_YYYYMMDD.log`.

## 🛠 Tools & Technologies

- **Appium** – Mobile automation
- **UiAutomator2** – Android automation engine
- **Python** – Test language
- **pytest** – Test framework
- **Appium Python Client** – Appium bindings
