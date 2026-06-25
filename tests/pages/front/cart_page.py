"""
购物车页 Page Object

URL: /cart
需要登录态
"""
import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from config.config import BASE_URL


class CartPage(BasePage):
    URL = f"{BASE_URL}/cart"

    # ── 顶栏 ──
    LOGO        = (By.CSS_SELECTOR, ".top-bar .logo")

    # ── 购物车表格 ──
    CART_TABLE  = (By.CSS_SELECTOR, ".cart-table")
    CART_ROWS   = (By.CSS_SELECTOR, ".cart-row")
    CART_HEADER = (By.CSS_SELECTOR, ".cart-header")

    # ── 全选 ──
    SELECT_ALL_CB = (By.CSS_SELECTOR, ".cart-header .el-checkbox")
    ROW_CB        = (By.CSS_SELECTOR, ".cart-row .el-checkbox")

    # ── 商品信息 ──
    G_NAME      = (By.CSS_SELECTOR, ".g-name")
    G_ATTR      = (By.CSS_SELECTOR, ".g-attr")
    COL_PRICE   = (By.CSS_SELECTOR, ".col-price")
    COL_NUM     = (By.CSS_SELECTOR, ".col-num .el-input__inner")
    COL_SUB     = (By.CSS_SELECTOR, ".col-sub")
    COL_ACT     = (By.CSS_SELECTOR, ".col-act .el-button")

    # ── 数量控件 ──
    NUM_INCREASE = (By.CSS_SELECTOR, ".el-input-number__increase")
    NUM_DECREASE = (By.CSS_SELECTOR, ".el-input-number__decrease")

    # ── 底部操作 ──
    DELETE_SELECTED_BTN = (By.XPATH, "//button[contains(.,'删除选中')]")
    KEEP_SHOP_LINK      = (By.LINK_TEXT, "继续购物")
    SUMMARY             = (By.CSS_SELECTOR, ".summary")
    SELECTED_COUNT      = (By.CSS_SELECTOR, ".summary b")
    TOTAL_PRICE         = (By.CSS_SELECTOR, ".total b")
    CHECKOUT_BTN        = (By.XPATH, "//button[contains(@class,'el-button--primary') and contains(.,'去结算')]")

    # ── 空状态 ──
    EMPTY              = (By.CSS_SELECTOR, ".el-empty")
    EMPTY_DESC         = (By.CSS_SELECTOR, ".el-empty__description")
    GO_SHOP_BTN        = (By.XPATH, "//button[contains(.,'去逛逛')]")

    # ── 确认对话框 ──
    CONFIRM_BOX        = (By.CSS_SELECTOR, ".el-message-box")
    CONFIRM_PRIMARY    = (By.CSS_SELECTOR, ".el-message-box__btns .el-button--primary")
    CONFIRM_CANCEL     = (By.CSS_SELECTOR, ".el-message-box__btns .el-button:not(.el-button--primary)")

    @allure.step("打开购物车")
    def open(self) -> None:
        super().open(self.URL)

    # ── 购物车状态 ──

    def get_item_count(self) -> int:
        return self.element_count(self.CART_ROWS)

    def is_empty(self) -> bool:
        return self.is_displayed(self.EMPTY)

    def get_empty_text(self) -> str:
        return self.get_text(self.EMPTY_DESC)

    # ── 全选 ──

    @allure.step("全选/取消全选")
    def toggle_select_all(self) -> None:
        self.click(self.SELECT_ALL_CB)

    def is_all_selected(self) -> bool:
        cb = self.find(self.SELECT_ALL_CB)
        return "is-checked" in cb.get_attribute("class")

    # ── 单行操作 ──

    @allure.step("切换第 {row_index} 行选中状态")
    def toggle_row_selection(self, row_index: int = 0) -> None:
        rows = self.find_all(self.CART_ROWS)
        if row_index < len(rows):
            cb = rows[row_index].find_element(By.CSS_SELECTOR, ".el-checkbox")
            cb.click()

    @allure.step("修改第 {row_index} 行数量为 {num}")
    def update_quantity(self, row_index: int, num: int) -> None:
        rows = self.find_all(self.CART_ROWS)
        if row_index < len(rows):
            num_input = rows[row_index].find_element(By.CSS_SELECTOR, ".el-input__inner")
            num_input.clear()
            num_input.send_keys(str(num))

    @allure.step("删除第 {row_index} 行")
    def delete_item(self, row_index: int = 0) -> None:
        rows = self.find_all(self.CART_ROWS)
        if row_index < len(rows):
            del_btn = rows[row_index].find_element(By.CSS_SELECTOR, ".col-act .el-button")
            del_btn.click()

    @allure.step("批量删除选中")
    def delete_selected(self, confirm: bool = True) -> None:
        self.click(self.DELETE_SELECTED_BTN)
        if confirm:
            self._pause(0.3)
            self.el_dialog_confirm()

    # ── 获取商品信息 ──

    def get_item_names(self) -> list:
        names = self.find_all(self.G_NAME)
        return [n.text for n in names]

    def get_selected_count(self) -> int:
        count_els = self.driver.find_elements(By.CSS_SELECTOR, ".summary b")
        if count_els:
            return int(count_els[0].text)
        return 0

    def get_total_price(self) -> str:
        return self.get_text(self.TOTAL_PRICE)

    # ── 结算 ──

    @allure.step("去结算")
    def go_checkout(self) -> None:
        self.click(self.CHECKOUT_BTN)

    def is_checkout_enabled(self) -> bool:
        btn = self.find(self.CHECKOUT_BTN)
        return btn.is_enabled()

    # ── 继续购物 ──

    def continue_shopping(self) -> None:
        self.click(self.KEEP_SHOP_LINK)

    def go_home(self) -> None:
        self.click(self.LOGO)
