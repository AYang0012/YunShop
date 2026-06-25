"""
后台订单管理页 Page Object（占位页）

URL: /admin/order
"""
import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from config.config import BASE_URL


class AdminOrderPage(BasePage):
    URL = f"{BASE_URL}/admin/order"

    PAGE_TITLE = (By.CSS_SELECTOR, "h1, h2, .page-title")

    @allure.step("打开订单管理")
    def open(self) -> None:
        super().open(self.URL)

    def is_order_page(self) -> bool:
        return "/admin/order" in self.current_url
