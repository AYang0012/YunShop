"""
订单确认页 Page Object

URL: /order/confirm
需要登录态
"""
import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.config import BASE_URL


class OrderConfirmPage(BasePage):
    URL = f"{BASE_URL}/order/confirm"

    # ── 地址 ──
    ADDRESS_SECTION = (By.CSS_SELECTOR, ".address-section")  # 根据实际结构调整
    ADDRESS_ITEM    = (By.CSS_SELECTOR, ".address-item")
    ADDRESS_ADD     = (By.CSS_SELECTOR, ".address-add")

    # ── 商品清单 ──
    GOODS_LIST      = (By.CSS_SELECTOR, ".order-goods-list, .goods-list")
    GOODS_ITEM      = (By.CSS_SELECTOR, ".order-goods-item, .goods-item")

    # ── 支付方式 ──
    PAY_NAME_ALIPAY = (By.XPATH, "//label[contains(.,'支付宝')]")
    PAY_NAME_WECHAT = (By.XPATH, "//label[contains(.,'微信')]")
    PAY_NAME_UNION  = (By.XPATH, "//label[contains(.,'银联')]")
    PAY_NAME_COD    = (By.XPATH, "//label[contains(.,'货到付款')]")

    # ── 配送方式 ──
    SHIPPING_NAME   = (By.XPATH, "//label[contains(.,'快递')]")

    # ── 备注 ──
    REMARK_INPUT    = (By.CSS_SELECTOR, "textarea, input[placeholder*='备注']")

    # ── 金额 ──
    TOTAL_AMOUNT    = (By.CSS_SELECTOR, ".total-amount, .order-total b")

    # ── 提交 ──
    SUBMIT_BTN      = (By.XPATH, "//button[contains(.,'提交订单')]")

    # ── 顶栏 ──
    LOGO            = (By.CSS_SELECTOR, ".top-bar .logo")
    CART_BTN        = (By.CSS_SELECTOR, ".top-bar .cart-btn")

    @allure.step("打开订单确认页")
    def open(self) -> None:
        super().open(self.URL)

    @allure.step("选择支付方式: {pay_name}")
    def select_pay_method(self, pay_name: str = "alipay") -> None:
        mapping = {
            "alipay": self.PAY_NAME_ALIPAY,
            "wechat": self.PAY_NAME_WECHAT,
            "union":  self.PAY_NAME_UNION,
            "cod":    self.PAY_NAME_COD,
        }
        locator = mapping.get(pay_name)
        if locator:
            self.click(locator)

    @allure.step("填写备注: {remark}")
    def type_remark(self, remark: str) -> None:
        self.type(self.REMARK_INPUT, remark)

    @allure.step("提交订单")
    def submit_order(self) -> None:
        self.click(self.SUBMIT_BTN)

    def get_total_amount(self) -> str:
        return self.get_text(self.TOTAL_AMOUNT)

    def is_confirm_page(self) -> bool:
        return "/order/confirm" in self.current_url
