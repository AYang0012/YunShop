"""
会员登录页 Page Object

URL: /login
"""
import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.config import BASE_URL


class LoginPage(BasePage):
    URL = f"{BASE_URL}/login"

    # ── 元素定位器 ──
    USERNAME_INPUT  = (By.CSS_SELECTOR, "input[placeholder*='手机号'][placeholder*='邮箱']")
    PASSWORD_INPUT  = (By.CSS_SELECTOR, "input[type='password'][placeholder='密码']")
    CAPTCHA_INPUT   = (By.CSS_SELECTOR, "input[placeholder='验证码']")
    CAPTCHA_BTN     = (By.CSS_SELECTOR, ".captcha-btn")
    SUBMIT_BTN      = (By.CSS_SELECTOR, "button.submit-btn, .el-button--primary[type='submit']")
    REGISTER_LINK   = (By.LINK_TEXT, "还没有账号？立即注册")
    HOME_LINK       = (By.LINK_TEXT, "返回首页")
    TITLE           = (By.CSS_SELECTOR, ".title")
    SUBTITLE        = (By.CSS_SELECTOR, ".subtitle")
    FORM_ERROR      = (By.CSS_SELECTOR, ".el-form-item__error")

    @allure.step("打开登录页")
    def open(self) -> None:
        super().open(self.URL)

    @allure.step("会员登录: username={username}")
    def login(self, username: str, password: str, captcha: str = "dev") -> None:
        """
        执行登录操作。

        Args:
            username: 手机号或邮箱
            password: 密码
            captcha: 验证码（开发环境默认 "dev" 跳过校验）
        """
        self.type(self.USERNAME_INPUT, username)
        self.type(self.PASSWORD_INPUT, password)

        # 先获取验证码
        self.click(self.CAPTCHA_BTN)
        self.wait_seconds(0.5)

        self.type(self.CAPTCHA_INPUT, captcha)
        self.click(self.SUBMIT_BTN)

    @allure.step("获取验证码")
    def get_captcha_text(self) -> str:
        """点击获取验证码按钮，返回验证码文本。"""
        self.click(self.CAPTCHA_BTN)
        self.wait_seconds(0.3)
        return self.get_text(self.CAPTCHA_BTN)

    def get_title_text(self) -> str:
        return self.get_text(self.TITLE)

    def get_form_errors(self) -> list:
        """获取所有表单校验错误信息。"""
        errors = self.driver.find_elements(*self.FORM_ERROR)
        return [el.text for el in errors] if errors else []

    def is_login_page(self) -> bool:
        return self.is_displayed(self.TITLE) and "登录" in self.get_text(self.TITLE)

    def go_register(self) -> None:
        self.click(self.REGISTER_LINK)

    def go_home(self) -> None:
        self.click(self.HOME_LINK)
