"""
后台商品添加/编辑页 Page Object

URL: /admin/goods/edit/:id?
"""
import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from config.config import BASE_URL


class AdminGoodsEditPage(BasePage):
    URL = f"{BASE_URL}/admin/goods/edit"

    # ── 表单字段 ──
    GOODS_NAME_INPUT   = (By.CSS_SELECTOR, "input[placeholder*='商品名称']")
    GOODS_SN_INPUT     = (By.CSS_SELECTOR, "input[placeholder*='编号']")
    SHOP_PRICE_INPUT   = (By.CSS_SELECTOR, "input[placeholder*='售价'], input[placeholder*='价格']")
    MARKET_PRICE_INPUT = (By.CSS_SELECTOR, "input[placeholder*='原价'], input[placeholder*='市场价']")
    STORE_COUNT_INPUT  = (By.CSS_SELECTOR, "input[placeholder*='库存']")
    GOODS_CONTENT_INPUT = (By.CSS_SELECTOR, "textarea")

    # ── 保存/取消 ──
    SAVE_BTN   = (By.XPATH, "//button[contains(.,'保存') or contains(.,'提交')]")
    CANCEL_BTN = (By.XPATH, "//button[contains(.,'取消') or contains(.,'返回')]")
    BACK_BTN   = (By.XPATH, "//button[contains(.,'返回')] | //a[contains(.,'返回')]")

    @allure.step("打开添加商品页")
    def open_new(self) -> None:
        super().open(self.URL)

    @allure.step("打开编辑商品页: id={goods_id}")
    def open_edit(self, goods_id: int) -> None:
        super().open(f"{self.URL}/{goods_id}")

    @allure.step("填写商品信息: {goods_name}")
    def fill_form(
        self,
        goods_name: str,
        goods_sn: str = "",
        shop_price: str = "",
        market_price: str = "",
        store_count: str = "",
        goods_content: str = "",
    ) -> None:
        self.type(self.GOODS_NAME_INPUT, goods_name)
        if goods_sn:
            self.type(self.GOODS_SN_INPUT, goods_sn)
        if shop_price:
            self.type(self.SHOP_PRICE_INPUT, shop_price)
        if market_price:
            self.type(self.MARKET_PRICE_INPUT, market_price)
        if store_count:
            self.type(self.STORE_COUNT_INPUT, store_count)
        if goods_content:
            self.type(self.GOODS_CONTENT_INPUT, goods_content)

    @allure.step("保存商品")
    def save(self) -> None:
        self.click(self.SAVE_BTN)

    @allure.step("取消")
    def cancel(self) -> None:
        self.click(self.CANCEL_BTN)

    def is_edit_page(self) -> bool:
        return "/admin/goods/edit" in self.current_url
