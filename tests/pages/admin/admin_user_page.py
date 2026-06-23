"""
后台会员管理页 Page Object（占位页）

URL: /admin/user
"""
import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.config import BASE_URL


class AdminUserPage(BasePage):
    URL = f"{BASE_URL}/admin/user"

    PAGE_TITLE = (By.CSS_SELECTOR, "h1, h2, .page-title")

    @allure.step("打开会员管理")
    def open(self) -> None:
        super().open(self.URL)

    def is_user_page(self) -> bool:
        return "/admin/user" in self.current_url
