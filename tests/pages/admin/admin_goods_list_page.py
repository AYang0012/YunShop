"""
后台商品管理列表页 Page Object

URL: /admin/goods
需要管理员登录
"""
import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from config.config import BASE_URL


class AdminGoodsListPage(BasePage):
    URL = f"{BASE_URL}/admin/goods"

    # ── 工具栏 ──
    ADD_BTN     = (By.XPATH, "//button[contains(.,'添加') or contains(.,'新增')]")
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[placeholder*='搜索']")
    SEARCH_BTN  = (By.XPATH, "//button[contains(.,'搜索')]")

    # ── 商品表格 ──
    GOODS_TABLE = (By.CSS_SELECTOR, ".el-table, table")
    TABLE_ROWS  = (By.CSS_SELECTOR, ".el-table__body tr.el-table__row, tbody tr")
    TABLE_CELLS = (By.CSS_SELECTOR, "td")
    GOODS_NAME_CELL = (By.CSS_SELECTOR, "td:first-child, td:nth-child(2)")

    # ── 操作 ──
    EDIT_BTN    = (By.XPATH, "//button[contains(.,'编辑')] | //a[contains(.,'编辑')]")
    DELETE_BTN  = (By.XPATH, "//button[contains(.,'删除')]")
    TOGGLE_BTN  = (By.XPATH, "//button[contains(.,'上架') or contains(.,'下架')]")

    # ── 分页 ──
    PAGINATION  = (By.CSS_SELECTOR, ".el-pagination")

    @allure.step("打开商品管理")
    def open(self) -> None:
        super().open(self.URL)

    @allure.step("点击添加商品")
    def click_add(self) -> None:
        self.click(self.ADD_BTN)

    @allure.step("搜索商品: {keyword}")
    def search(self, keyword: str) -> None:
        self.type(self.SEARCH_INPUT, keyword)
        self.click(self.SEARCH_BTN)

    def get_goods_count(self) -> int:
        """获取当前页商品数量。"""
        try:
            return self.element_count(self.TABLE_ROWS)
        except Exception:
            return 0

    def get_goods_names(self) -> list:
        """获取当前页所有商品名称。"""
        rows = self.find_all(self.TABLE_ROWS)
        names = []
        for row in rows:
            cells = row.find_elements(*self.TABLE_CELLS)
            if cells:
                names.append(cells[1].text if len(cells) > 1 else cells[0].text)
        return names

    @allure.step("编辑第 {index} 个商品")
    def click_edit(self, index: int = 0) -> None:
        rows = self.find_all(self.TABLE_ROWS)
        if index < len(rows):
            edit_btns = rows[index].find_elements(By.XPATH, ".//button[contains(.,'编辑')] | .//a[contains(.,'编辑')]")
            if edit_btns:
                edit_btns[0].click()

    @allure.step("删除第 {index} 个商品")
    def click_delete(self, index: int = 0) -> None:
        rows = self.find_all(self.TABLE_ROWS)
        if index < len(rows):
            del_btns = rows[index].find_elements(By.XPATH, ".//button[contains(.,'删除')]")
            if del_btns:
                del_btns[0].click()
                self._pause(0.3)
                self.el_dialog_confirm()

    @allure.step("切换第 {index} 个商品上下架")
    def toggle_sale(self, index: int = 0) -> None:
        rows = self.find_all(self.TABLE_ROWS)
        if index < len(rows):
            toggle_btns = rows[index].find_elements(By.XPATH, ".//button[contains(.,'上架') or contains(.,'下架')]")
            if toggle_btns:
                toggle_btns[0].click()
