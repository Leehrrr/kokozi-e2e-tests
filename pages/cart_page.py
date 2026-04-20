import re
from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from config import BASE_URL


class CartPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    def goto(self):
        self.navigate(f"{BASE_URL}cart")
        self.page.wait_for_timeout(2000)

    def open_cart_menu(self):
        self.page.get_by_role("menu").filter(
            has_text=re.compile(r"^\d+$")
        ).click()

    def clear(self):
        # 홈으로 이동 후 장바구니 배지 확인
        self.page.goto(BASE_URL, wait_until="domcontentloaded")
        self.page.wait_for_timeout(1000)
        cart_badge = self.page.get_by_role("menu").filter(
            has_text=re.compile(r"^\d+$")
        )
        if not cart_badge.is_visible():
            return
        cart_badge.click()
        while not self.page.get_by_role("link", name="상품 보러 가기").is_visible():
            self.page.get_by_role("button").nth(1).click()
            self.page.wait_for_timeout(500)
            self.page.get_by_role("button", name="삭제").wait_for(state="visible")
            self.page.get_by_role("button", name="삭제").click()
            self.page.wait_for_timeout(1000)

    def assert_product_visible(self, product_name: str):
        expect(
            self.page.get_by_text(product_name).first
        ).to_be_visible(timeout=10000)

    def assert_product_count(self, product_name: str, expected_qty: int):
        qty = self.page.locator(
            f".cart-item:has-text('{product_name}') input[type='number']"
        )
        expect(qty).to_have_value(str(expected_qty), timeout=10000)

    def screenshot(self, path: str):
        self.page.screenshot(path=path)
