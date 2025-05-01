from playwright.sync_api import sync_playwright
import pytest

@pytest.fixture
def context():
    return {}

pytest_plugins = [
    "framework.common_steps",
]

# Playwright browser fixture
@pytest.fixture
def playwright_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        yield page
        browser.close()

# Hook to take screenshots on failure
import allure
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        if "playwright_page" in item.fixturenames:
            page = item.funcargs["playwright_page"]
            screenshot_path = "screenshots/failed_test.png"
            page.screenshot(path=screenshot_path)
            with open(screenshot_path, "rb") as f:
                allure.attach(f.read(), name="Failed Screenshot", attachment_type=allure.attachment_type.PNG)
