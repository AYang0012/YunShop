"""
会员注册页 Page Object

URL: /register
"""
import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.config import BASE_URL


class RegisterPage(BasePage):
    URL = f"{BASE_URL}/register"

    # ── 元素定位器 ──
    MOBILE_TAB      = (By.XPATH, "//label[contains(@class,'el-radio-button')]/span[contains(text(),'手机号注册')]")
    EMAIL_TAB       = (By.XPATH, "//label[contains(@class,'el-radio-button')]/span[contains(text(),'邮箱注册')]")
    ACCOUNT_INPUT   = (By.CSS_SELECTOR, "input[placeholder*='请输入']")
    PASSWORD_INPUT  = (By.CSS_SELECTOR, "input[type='password'][placeholder*='密码'][placeholder*='6-16']")
    CONFIRM_INPUT   = (By.CSS_SELECTOR, "input[type='password'][placeholder='确认密码']")
    REFERRER_INPUT  = (By.CSS_SELECTOR, "input[placeholder*='推荐人']")
    PROTOCOL_CB     = (By.CSS_SELECTOR, ".el-checkbox")
    PROTOCOL_LABEL  = (By.CSS_SELECTOR, ".el-checkbox__label")
    SUBMIT_BTN      = (By.CSS_SELECTOR, "button.el-button--primary[type='submit']")
    LOGIN_LINK      = (By.LINK_TEXT, "已有账号？立即登录")
    HOME_LINK       = (By.LINK_TEXT, "返回首页")
    TITLE           = (By.CSS_SELECTOR, ".title")
    FORM_ERROR      = (By.CSS_SELECTOR, ".el-form-item__error")

    @allure.step("打开注册页")
    def open(self) -> None:
        super().open(self.URL)

    @allure.step("注册: account={account}, type={register_type}")
    def register(
        self,
        account: str,
        password: str,
        confirm_password: str = None,
        register_type: str = "mobile",
        referrer: str = "",
        agree_protocol: bool = True,
    ) -> None:
        """
        执行注册操作。

        Args:
            account: 手机号或邮箱
            password: 密码
            confirm_password: 确认密码（默认与 password 相同）
            register_type: "mobile" 或 "email"
            referrer: 推荐人手机号
            agree_protocol: 是否勾选协议
        """
        if confirm_password is None:
            confirm_password = password

        # 选择注册方式
        if register_type == "email":
            self.click(self.EMAIL_TAB)

        self.type(self.ACCOUNT_INPUT, account)
        self.type(self.PASSWORD_INPUT, password)
        self.type(self.CONFIRM_INPUT, confirm_password)

        if referrer:
            self.type(self.REFERRER_INPUT, referrer)

        if agree_protocol:
            self.checkbox_check(self.PROTOCOL_CB, check=True)

        self.click(self.SUBMIT_BTN)

    @allure.step("切换到邮箱注册")
    def switch_to_email(self) -> None:
        self.click(self.EMAIL_TAB)

    @allure.step("切换到手机号注册")
    def switch_to_mobile(self) -> None:
        self.click(self.MOBILE_TAB)

    def get_title_text(self) -> str:
        return self.get_text(self.TITLE)

    def get_form_errors(self) -> list:
        errors = self.driver.find_elements(*self.FORM_ERROR)
        return [el.text for el in errors] if errors else []

    def is_register_page(self) -> bool:
        return "注册" in self.get_text(self.TITLE)

    def go_login(self) -> None:
        self.click(self.LOGIN_LINK)
