import pytest
from playwright.sync_api import Page
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.login_page import LoginPage
from config import (
    PRODUCT_A_URL, PRODUCT_A_NAME,
    PRODUCT_B_URL, PRODUCT_B_NAME,
    MEMBER_EMAIL, MEMBER_PASSWORD,
)


def test_cart_merge_on_login(page: Page):
    product_page = ProductPage(page)
    cart_page    = CartPage(page)
    login_page   = LoginPage(page)

    # ════════════════════════════════════════════════════════
    # [Setup] 회원 장바구니에 상품 B 세팅
    # ════════════════════════════════════════════════════════

    # 1. 로그인
    login_page.goto()
    login_page.login(MEMBER_EMAIL, MEMBER_PASSWORD)

    # 2. 장바구니 초기화 (기존 상품 전체 삭제)
    cart_page.clear()

    # 3. 상품 B 담기
    product_page.goto(PRODUCT_B_URL)
    product_page.add_to_cart()
    product_page.close_add_to_cart_dialog()

    # 4. 로그아웃
    login_page.logout()

    # ════════════════════════════════════════════════════════
    # [Test] 비회원 상품 A 담기 → 로그인 → 병합 확인
    # ════════════════════════════════════════════════════════

    # [CRT-MG-01] 비회원 상태에서 상품 A 장바구니 담기
    product_page.goto(PRODUCT_A_URL)
    product_page.add_to_cart()
    product_page.close_add_to_cart_dialog()

    # [CRT-FL-05] 헤더 장바구니 메뉴에서 상품 A 노출 확인
    cart_page.open_cart_menu()
    cart_page.assert_product_visible(PRODUCT_A_NAME)
    page.wait_for_timeout(1000)
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)

    # [CRT-MG-02] 회원 계정으로 로그인
    login_page.goto()
    login_page.login(MEMBER_EMAIL, MEMBER_PASSWORD)

    # [CRT-MG-02] 병합 확인: 상품 A + 상품 B 모두 노출
    cart_page.goto()
    cart_page.screenshot(path="cart_merge_result.png")
    cart_page.assert_product_visible(PRODUCT_A_NAME)
    cart_page.assert_product_visible(PRODUCT_B_NAME)

