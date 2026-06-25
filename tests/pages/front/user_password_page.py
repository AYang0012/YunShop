"""
修改密码页 Page Object

URL: /user/password
需要登录态
"""
import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from config.config import BASE_URL


class UserPasswordPage(BasePage):
    URL = f"{BASE_URL}/user/password"

    # ── 输入 ──
    OLD_PASSWORD_INPUT  = (By.CSS_SELECTOR, "input[placeholder*='原密码'], input[placeholder*='旧密码']")
    NEW_PASSWORD_INPUT  = (By.CSS_SELECTOR, "input[placeholder*='新密码']")
    CONFIRM_PASSWORD_INPUT = (By.CSS_SELECTOR, "input[placeholder*='确认密码'], input[placeholder*='再次输入']")

    # ── 提交 ──
    SUBMIT_BTN          = (By.XPATH, "//button[contains(.,'修改') or contains(.,'确认修改') or contains(.,'提交')]")

    @allure.step("打开修改密码")
    def open(self) -> None:
        super().open(self.URL)

    @allure.step("修改密码")
    def change_password(
        self,
        old_password: str,
        new_password: str,
        confirm_password: str = None,
    ) -> None:
        if confirm_password is None:
            confirm_password = new_password

        self.type(self.OLD_PASSWORD_INPUT, old_password)
        self.type(self.NEW_PASSWORD_INPUT, new_password)
        self.type(self.CONFIRM_PASSWORD_INPUT, confirm_password)
        self.click(self.SUBMIT_BTN)
