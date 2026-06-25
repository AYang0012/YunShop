"""
商品列表页 Page Object

URL: /goods/list?catId=...
"""
import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from config.config import BASE_URL


class GoodsListPage(BasePage):
    URL = f"{BASE_URL}/goods/list"

    # ── 搜索 ──
    SEARCH_INPUT = (By.CSS_SELECTOR, ".search-input input, .search-input .el-input__inner")
    SEARCH_BTN   = (By.CSS_SELECTOR, ".search-input .el-button, .el-input-group__append .el-button")

    # ── 排序栏 ──
    SORT_BAR     = (By.CSS_SELECTOR, ".sort-bar")
    SORT_DEFAULT = (By.XPATH, "//div[contains(@class,'sort-bar')]/span[contains(text(),'综合')]")
    SORT_SALES   = (By.XPATH, "//div[contains(@class,'sort-bar')]/span[contains(text(),'销量')]")
    SORT_PRICE   = (By.XPATH, "//div[contains(@class,'sort-bar')]/span[contains(text(),'价格')]")
    SORT_TIME    = (By.XPATH, "//div[contains(@class,'sort-bar')]/span[contains(text(),'新品')]")
    PAGE_SIZE_12 = (By.XPATH, "//div[contains(@class,'page-size')]/span[text()='12条/页']")
    PAGE_SIZE_24 = (By.XPATH, "//div[contains(@class,'page-size')]/span[text()='24条/页']")
    PAGE_SIZE_48 = (By.XPATH, "//div[contains(@class,'page-size')]/span[text()='48条/页']")

    # ── 商品网格 ──
    GOODS_GRID   = (By.CSS_SELECTOR, ".goods-grid")
    G_CARD       = (By.CSS_SELECTOR, ".g-card")
    G_NAME       = (By.CSS_SELECTOR, ".g-name")
    G_PRICE      = (By.CSS_SELECTOR, ".price")
    G_SALES      = (By.CSS_SELECTOR, ".sales")
    G_TIME       = (By.CSS_SELECTOR, ".g-time")

    # ── 分页 ──
    PAGINATION   = (By.CSS_SELECTOR, ".el-pagination")
    PAGE_PREV    = (By.CSS_SELECTOR, ".btn-prev")
    PAGE_NEXT    = (By.CSS_SELECTOR, ".btn-next")
    PAGE_NUMBERS = (By.CSS_SELECTOR, ".el-pager li.number")

    # ── 空状态 ──
    EMPTY        = (By.CSS_SELECTOR, ".el-empty")
    EMPTY_DESC   = (By.CSS_SELECTOR, ".el-empty__description")

    # ── 顶栏 ──
    LOGO         = (By.CSS_SELECTOR, ".top-bar .logo")
    CART_BTN     = (By.CSS_SELECTOR, ".top-bar .cart-btn")

    @allure.step("打开商品列表页")
    def open(self, cat_id: int = None, keyword: str = None) -> None:
        params = []
        if cat_id:
            params.append(f"catId={cat_id}")
        if keyword:
            params.append(f"keyword={keyword}")
        url = self.URL
        if params:
            url += "?" + "&".join(params)
        super().open(url)

    @allure.step("搜索: {keyword}")
    def search(self, keyword: str) -> None:
        self.type(self.SEARCH_INPUT, keyword)
        self.click(self.SEARCH_BTN)

    def get_search_keyword(self) -> str:
        return self.get_value(self.SEARCH_INPUT)

    # ── 排序 ──

    @allure.step("点击「综合」排序")
    def sort_by_default(self) -> None:
        self.click(self.SORT_DEFAULT)

    @allure.step("点击「销量」排序")
    def sort_by_sales(self) -> None:
        self.click(self.SORT_SALES)

    @allure.step("点击「价格」排序")
    def sort_by_price(self) -> None:
        self.click(self.SORT_PRICE)

    @allure.step("点击「新品」排序")
    def sort_by_time(self) -> None:
        self.click(self.SORT_TIME)

    @allure.step("切换每页: {size} 条")
    def set_page_size(self, size: int) -> None:
        mapping = {12: self.PAGE_SIZE_12, 24: self.PAGE_SIZE_24, 48: self.PAGE_SIZE_48}
        locator = mapping.get(size)
        if locator:
            self.click(locator)

    # ── 商品 ──

    def get_goods_count(self) -> int:
        return self.element_count(self.G_CARD)

    def get_goods_names(self) -> list:
        return [el.text for el in self.find_all(self.G_NAME)]

    def get_goods_prices(self) -> list:
        return [el.text for el in self.find_all(self.G_PRICE)]

    def click_goods(self, index: int = 0) -> None:
        cards = self.find_all(self.G_CARD)
        if index < len(cards):
            cards[index].click()

    def is_empty(self) -> bool:
        return self.is_displayed(self.EMPTY)

    # ── 分页 ──

    def get_current_page(self) -> int:
        active = self.driver.find_element(By.CSS_SELECTOR, ".el-pager li.number.active")
        return int(active.text)

    def click_next_page(self) -> None:
        self.click(self.PAGE_NEXT)

    def click_prev_page(self) -> None:
        self.click(self.PAGE_PREV)

    def click_page(self, page_num: int) -> None:
        numbers = self.find_all(self.PAGE_NUMBERS)
        for n in numbers:
            if n.text == str(page_num):
                n.click()
                return

    # ── 导航 ──

    def go_home(self) -> None:
        self.click(self.LOGO)

    def go_cart(self) -> None:
        self.click(self.CART_BTN)
