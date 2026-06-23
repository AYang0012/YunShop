"""
后台分类管理页 Page Object（占位页）

URL: /admin/category
"""
import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.config import BASE_URL


class AdminCategoryPage(BasePage):
    URL = f"{BASE_URL}/admin/category"

    # ── 占位内容 ──
    PAGE_TITLE = (By.CSS_SELECTOR, "h1, h2, .page-title")

    @allure.step("打开分类管理")
    def open(self) -> None:
        super().open(self.URL)

    def is_category_page(self) -> bool:
        return "/admin/category" in self.current_url
