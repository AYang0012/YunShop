"""
我的订单页 Page Object

URL: /user/orders
需要登录态
"""
import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.config import BASE_URL


class UserOrdersPage(BasePage):
    URL = f"{BASE_URL}/user/orders"

    # ── 订单状态 Tab ──
    TAB_ALL       = (By.XPATH, "//span[text()='全部' or text()='所有订单']")
    TAB_PENDING   = (By.XPATH, "//span[text()='待付款']")
    TAB_PAID      = (By.XPATH, "//span[text()='待发货']")
    TAB_SHIPPED   = (By.XPATH, "//span[text()='待收货']")
    TAB_COMPLETED = (By.XPATH, "//span[text()='已完成']")
    TAB_CANCELLED = (By.XPATH, "//span[text()='已取消']")

    # ── 订单列表 ──
    ORDER_ITEM    = (By.CSS_SELECTOR, ".order-item, .order-card")
    ORDER_SN      = (By.CSS_SELECTOR, ".order-sn")
    ORDER_STATUS  = (By.CSS_SELECTOR, ".order-status")
    ORDER_AMOUNT  = (By.CSS_SELECTOR, ".order-amount")

    # ── 操作按钮 ──
    PAY_BTN       = (By.XPATH, "//button[contains(.,'付款') or contains(.,'支付')]")
    CANCEL_BTN    = (By.XPATH, "//button[contains(.,'取消')]")
    RECEIVE_BTN   = (By.XPATH, "//button[contains(.,'确认收货')]")
    DETAIL_BTN    = (By.XPATH, "//button[contains(.,'详情')] | //a[contains(.,'详情')]")

    # ── 空状态 ──
    EMPTY         = (By.CSS_SELECTOR, ".el-empty")

    @allure.step("打开我的订单")
    def open(self) -> None:
        super().open(self.URL)

    # ── Tab 切换 ──

    @allure.step("筛选: {tab_name}")
    def filter_by_status(self, status: str) -> None:
        tab_map = {
            "all":       self.TAB_ALL,
            "PENDING":   self.TAB_PENDING,
            "PAID":      self.TAB_PAID,
            "SHIPPED":   self.TAB_SHIPPED,
            "COMPLETED": self.TAB_COMPLETED,
            "CANCELLED": self.TAB_CANCELLED,
        }
        locator = tab_map.get(status)
        if locator:
            self.click(locator)

    # ── 订单操作 ──

    def get_order_count(self) -> int:
        return self.element_count(self.ORDER_ITEM)

    def is_empty(self) -> bool:
        return self.is_displayed(self.EMPTY)

    def get_order_sns(self) -> list:
        return [el.text for el in self.find_all(self.ORDER_SN)]

    @allure.step("订单详情: 第 {index} 个")
    def click_order_detail(self, index: int = 0) -> None:
        items = self.find_all(self.ORDER_ITEM)
        if index < len(items):
            detail_links = items[index].find_elements(By.XPATH, ".//button[contains(.,'详情')] | .//a[contains(.,'详情')]")
            if detail_links:
                detail_links[0].click()

    @allure.step("支付: 第 {index} 个订单")
    def pay_order(self, index: int = 0) -> None:
        items = self.find_all(self.ORDER_ITEM)
        if index < len(items):
            pay_btns = items[index].find_elements(By.XPATH, ".//button[contains(.,'付款') or contains(.,'支付')]")
            if pay_btns:
                pay_btns[0].click()

    @allure.step("取消: 第 {index} 个订单")
    def cancel_order(self, index: int = 0) -> None:
        items = self.find_all(self.ORDER_ITEM)
        if index < len(items):
            cancel_btns = items[index].find_elements(By.XPATH, ".//button[contains(.,'取消')]")
            if cancel_btns:
                cancel_btns[0].click()

    @allure.step("确认收货: 第 {index} 个订单")
    def confirm_receive(self, index: int = 0) -> None:
        items = self.find_all(self.ORDER_ITEM)
        if index < len(items):
            receive_btns = items[index].find_elements(By.XPATH, ".//button[contains(.,'确认收货')]")
            if receive_btns:
                receive_btns[0].click()
