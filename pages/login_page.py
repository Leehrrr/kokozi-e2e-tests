from playwright.sync_api import Page
from pages.base_page import BasePage
from config import BASE_URL


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.login_btn       = page.get_by_role("button", name="로그인")
        self.kakao_btn       = page.locator("div").filter(has_text="카카오로 시작하기").nth(2)
        self.email_input     = page.get_by_role("textbox", name="계정 정보 입력")
        self.password_input  = page.get_by_role("textbox", name="비밀번호 입력")
        self.kakao_login_btn = page.get_by_role("button", name="로그인", exact=True)

    def goto(self):
        self.navigate(BASE_URL)

    def login(self, email: str, password: str):
        import re
        # 팝업 닫기 (오늘은 그만 보기)
        try:
            popup_btn = self.page.get_by_role("button", name="오늘은 그만 보기")
            popup_btn.wait_for(state="visible", timeout=5000)
            popup_btn.click()
        except Exception:
            pass

        self.login_btn.click()
        self.kakao_btn.wait_for(state="visible")
        self.kakao_btn.click()
        # 카카오 세션 저장 시 이메일/비밀번호 폼이 뜨지 않을 수 있으므로 try-except 처리
        try:
            self.email_input.wait_for(state="visible", timeout=10000)
            self.email_input.fill(email)
            self.email_input.press("Tab")
            self.page.get_by_role("button", name="입력 내용 지우기").press("Tab")
            self.password_input.fill(password)
            self.kakao_login_btn.click()
        except Exception:
            pass  # 세션이 유효해 자동 로그인된 경우
        self.wait_for_url_contains("kokozi.com/kr", timeout=30000)
        self.page.wait_for_load_state("domcontentloaded")
        self.page.wait_for_timeout(1000)

    def logout(self):
        import re
        self.page.get_by_role("menu").filter(has_text=re.compile(r"^$")).nth(1).click()
        self.page.get_by_role("button", name="로그아웃").click()
        self.page.get_by_role("button", name="로그아웃").nth(1).click()
        self.page.wait_for_timeout(1000)
