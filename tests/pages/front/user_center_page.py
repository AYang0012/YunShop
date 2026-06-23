"""
用户中心页 Page Object

URL: /user
需要登录态
"""
import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.config import BASE_URL


class UserCenterPage(BasePage):
    URL = f"{BASE_URL}/user"

    # ── 导航菜单 ──
    NAV_ORDERS    = (By.XPATH, "//a[contains(@href,'/user/orders') or contains(text(),'我的订单')]")
    NAV_ADDRESS   = (By.XPATH, "//a[contains(@href,'/user/address') or contains(text(),'收货地址')]")
    NAV_PROFILE   = (By.XPATH, "//a[contains(@href,'/user/profile') or contains(text(),'个人信息')]")
    NAV_PASSWORD  = (By.XPATH, "//a[contains(@href,'/user/password') or contains(text(),'修改密码')]")

    # ── 顶栏 ──
    LOGO          = (By.CSS_SELECTOR, ".top-bar .logo")

    @allure.step("打开用户中心")
    def open(self) -> None:
        super().open(self.URL)

    @allure.step("导航到「我的订单」")
    def go_orders(self) -> None:
        self.click(self.NAV_ORDERS)

    @allure.step("导航到「收货地址」")
    def go_address(self) -> None:
        self.click(self.NAV_ADDRESS)

    @allure.step("导航到「个人信息」")
    def go_profile(self) -> None:
        self.click(self.NAV_PROFILE)

    @allure.step("导航到「修改密码」")
    def go_password(self) -> None:
        self.click(self.NAV_PASSWORD)

    def is_user_center(self) -> bool:
        return "/user" in self.current_url

    def go_home(self) -> None:
        self.click(self.LOGO)
