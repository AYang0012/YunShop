"""
后台管理框架页 Page Object

URL: /admin (嵌套路由，默认显示 Dashboard)
"""
import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from config.config import BASE_URL


class AdminIndexPage(BasePage):
    URL = f"{BASE_URL}/admin"

    # ── 侧边栏菜单 ──
    SIDEBAR       = (By.CSS_SELECTOR, ".el-menu, .sidebar")
    MENU_GOODS    = (By.XPATH, "//li[contains(@class,'el-menu-item')]/span[text()='商品管理']/.. | //a[contains(@href,'/admin/goods')]")
    MENU_CATEGORY = (By.XPATH, "//li[contains(@class,'el-menu-item')]/span[text()='分类管理']/.. | //a[contains(@href,'/admin/category')]")
    MENU_ORDER    = (By.XPATH, "//li[contains(@class,'el-menu-item')]/span[text()='订单管理']/.. | //a[contains(@href,'/admin/order')]")
    MENU_USER     = (By.XPATH, "//li[contains(@class,'el-menu-item')]/span[text()='会员管理']/.. | //a[contains(@href,'/admin/user')]")
    MENU_DASHBOARD = (By.XPATH, "//li[contains(@class,'el-menu-item')]/span[text()='仪表盘']/.. | //span[text()='仪表盘']/..")

    # ── 顶部 ──
    HEADER        = (By.CSS_SELECTOR, ".el-header, .admin-header")
    LOGOUT_BTN    = (By.XPATH, "//button[contains(.,'退出')] | //span[contains(.,'退出')] | //a[contains(.,'退出')]")
    USERNAME_TEXT = (By.CSS_SELECTOR, ".username, .admin-name")

    # ── 主内容区 ──
    MAIN_CONTENT  = (By.CSS_SELECTOR, ".el-main, .main-content")

    @allure.step("打开后台首页")
    def open(self) -> None:
        super().open(self.URL)

    # ── 导航 ──

    @allure.step("导航到「商品管理」")
    def go_goods(self) -> None:
        self.click(self.MENU_GOODS)

    @allure.step("导航到「分类管理」")
    def go_category(self) -> None:
        self.click(self.MENU_CATEGORY)

    @allure.step("导航到「订单管理」")
    def go_order(self) -> None:
        self.click(self.MENU_ORDER)

    @allure.step("导航到「会员管理」")
    def go_user(self) -> None:
        self.click(self.MENU_USER)

    @allure.step("导航到「仪表盘」")
    def go_dashboard(self) -> None:
        self.click(self.MENU_DASHBOARD)

    # ── 状态 ──

    def is_admin_page(self) -> bool:
        return "/admin" in self.current_url

    @allure.step("退出登录")
    def logout(self) -> None:
        self.click(self.LOGOUT_BTN)
