import re
from playwright.sync_api import Page, expect


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str):
        self.page.goto(url, wait_until="domcontentloaded")
        self.page.wait_for_timeout(1000)

    def wait_for_url_contains(self, keyword: str, timeout: int = 15000):
        expect(self.page).to_have_url(re.compile(re.escape(keyword)), timeout=timeout)
