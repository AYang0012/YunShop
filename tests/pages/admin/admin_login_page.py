"""
后台登录页 Page Object

URL: /admin/login
"""
import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from config.config import BASE_URL


class AdminLoginPage(BasePage):
    URL = f"{BASE_URL}/admin/login"

    # ── 元素 ──
    USERNAME_INPUT = (By.CSS_SELECTOR, "input[placeholder*='管理员']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[type='password']")
    SUBMIT_BTN     = (By.CSS_SELECTOR, "button.el-button--primary, .submit-btn")
    TITLE          = (By.CSS_SELECTOR, "h1")
    FORM_ERROR     = (By.CSS_SELECTOR, ".el-form-item__error")

    @allure.step("打开后台登录页")
    def open(self) -> None:
        super().open(self.URL)

    @allure.step("管理员登录: {username}")
    def login(self, username: str = "admin", password: str = "admin123") -> None:
        self.type(self.USERNAME_INPUT, username)
        self.type(self.PASSWORD_INPUT, password)
        self.click(self.SUBMIT_BTN)

    def get_title(self) -> str:
        return self.get_text(self.TITLE)

    def is_login_page(self) -> bool:
        return self.is_displayed(self.TITLE) and "后台" in self.get_text(self.TITLE)

    def get_form_errors(self) -> list:
        errors = self.driver.find_elements(*self.FORM_ERROR)
        return [el.text for el in errors] if errors else []
