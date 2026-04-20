import re
from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class ProductPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.add_to_cart_btn    = page.get_by_test_id("add_to_cart-upper")
        self.add_to_cart_dialog = page.get_by_test_id("add-to-cart-result")

    def goto(self, url: str):
        self.navigate(url)
        # 팝업이 뜨면 닫기
        try:
            popup = self.page.get_by_role("button", name="오늘은 그만 보기")
            popup.wait_for(state="visible", timeout=3000)
            popup.click()
        except Exception:
            pass

    def add_to_cart(self):
        self.add_to_cart_btn.scroll_into_view_if_needed()
        self.add_to_cart_btn.wait_for(state="visible")
        self.add_to_cart_btn.click()
        self.add_to_cart_dialog.wait_for(state="visible", timeout=10000)

    def close_add_to_cart_dialog(self):
        self.add_to_cart_dialog.get_by_role("button").filter(
            has_text=re.compile(r"^$")
        ).click()
        self.page.wait_for_timeout(1000)
