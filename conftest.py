import pytest
from playwright.sync_api import Playwright


@pytest.fixture(scope="function")
def page(playwright: Playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    pg = context.new_page()
    yield pg
    context.close()
    browser.close()
