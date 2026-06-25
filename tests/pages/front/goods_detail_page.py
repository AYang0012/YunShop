"""
商品详情页 Page Object

URL: /goods/detail/{goodsId}
"""
import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from config.config import BASE_URL


class GoodsDetailPage(BasePage):

    @staticmethod
    def url_for(goods_id: int) -> str:
        return f"{BASE_URL}/goods/detail/{goods_id}"

    # ── 元素定位器 ──
    MAIN_IMG        = (By.CSS_SELECTOR, ".main-img")
    GOODS_TITLE     = (By.CSS_SELECTOR, ".goods-title")
    GOODS_DESC      = (By.CSS_SELECTOR, ".desc")
    SHOP_PRICE      = (By.CSS_SELECTOR, ".shop-price")
    MARKET_PRICE    = (By.CSS_SELECTOR, ".market-price")
    META_SALES      = (By.XPATH, "//div[contains(@class,'meta')]/span[1]")
    META_STORE      = (By.XPATH, "//div[contains(@class,'meta')]/span[2]")

    # ── 数量输入（Element Plus InputNumber） ──
    NUM_INPUT       = (By.CSS_SELECTOR, ".el-input-number .el-input__inner")
    NUM_INCREASE    = (By.CSS_SELECTOR, ".el-input-number__increase")
    NUM_DECREASE    = (By.CSS_SELECTOR, ".el-input-number__decrease")

    # ── 操作按钮 ──
    ADD_TO_CART_BTN = (By.XPATH, "//button[contains(@class,'el-button--primary')]/span[contains(text(),'加入购物车')]/..")
    BUY_NOW_BTN     = (By.XPATH, "//button[contains(@class,'el-button--danger')]/span[contains(text(),'立即购买')]/..")

    # ── 商品详情 ──
    DETAIL_CONTENT  = (By.CSS_SELECTOR, ".detail-content")
    DETAIL_HEADING  = (By.CSS_SELECTOR, ".detail-content h3")

    # ── 顶栏 ──
    LOGO            = (By.CSS_SELECTOR, ".top-bar .logo")
    CART_BTN        = (By.CSS_SELECTOR, ".top-bar .cart-btn")

    @allure.step("打开商品详情: goodsId={goods_id}")
    def open(self, goods_id: int = 1) -> None:
        super().open(self.url_for(goods_id))

    # ── 信息读取 ──

    def get_goods_name(self) -> str:
        return self.get_text(self.GOODS_TITLE)

    def get_shop_price(self) -> str:
        return self.get_text(self.SHOP_PRICE)

    def get_market_price(self) -> str:
        try:
            return self.get_text(self.MARKET_PRICE)
        except Exception:
            return ""

    def get_store_count(self) -> str:
        return self.get_text(self.META_STORE)

    def get_sales_count(self) -> str:
        return self.get_text(self.META_SALES)

    # ── 数量操作 ──

    def get_buy_quantity(self) -> int:
        return int(self.get_value(self.NUM_INPUT))

    def set_quantity(self, num: int) -> None:
        """直接输入数量。"""
        self.type(self.NUM_INPUT, str(num))

    def increase_quantity(self, times: int = 1) -> None:
        for _ in range(times):
            self.click(self.NUM_INCREASE)

    def decrease_quantity(self, times: int = 1) -> None:
        for _ in range(times):
            self.click(self.NUM_DECREASE)

    # ── 操作 ──

    @allure.step("加入购物车")
    def add_to_cart(self) -> None:
        self.click(self.ADD_TO_CART_BTN)

    @allure.step("立即购买")
    def buy_now(self) -> None:
        self.click(self.BUY_NOW_BTN)

    # ── 页面判断 ──

    def is_detail_page(self) -> bool:
        return self.wait_for_url_contains("/goods/detail/")

    def has_detail_content(self) -> bool:
        return self.is_displayed(self.DETAIL_CONTENT)

    def go_cart(self) -> None:
        self.click(self.CART_BTN)

    def go_home(self) -> None:
        self.click(self.LOGO)
