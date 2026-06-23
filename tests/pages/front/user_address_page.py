"""
收货地址页 Page Object

URL: /user/address
需要登录态
"""
import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.config import BASE_URL


class UserAddressPage(BasePage):
    URL = f"{BASE_URL}/user/address"

    # ── 地址列表 ──
    ADDRESS_ITEM    = (By.CSS_SELECTOR, ".address-item, .address-card")
    ADDRESS_ADD_BTN = (By.XPATH, "//button[contains(.,'新增') or contains(.,'添加')]")
    SET_DEFAULT_BTN = (By.XPATH, "//button[contains(.,'默认')]")
    EDIT_BTN        = (By.XPATH, "//button[contains(.,'编辑')]")
    DELETE_BTN      = (By.XPATH, "//button[contains(.,'删除')]")

    # ── 表单 ──
    CONSIGNEE_INPUT = (By.CSS_SELECTOR, "input[placeholder*='收货人'], input[placeholder*='姓名']")
    MOBILE_INPUT    = (By.CSS_SELECTOR, "input[placeholder*='手机'], input[placeholder*='电话']")
    PROVINCE_INPUT  = (By.CSS_SELECTOR, "input[placeholder*='省']")
    CITY_INPUT      = (By.CSS_SELECTOR, "input[placeholder*='市']")
    DISTRICT_INPUT  = (By.CSS_SELECTOR, "input[placeholder*='区']")
    ADDRESS_INPUT   = (By.CSS_SELECTOR, "input[placeholder*='详细地址'], textarea[placeholder*='地址']")
    SAVE_BTN        = (By.XPATH, "//button[contains(.,'保存') or contains(.,'确定')]")

    # ── 空状态 ──
    EMPTY           = (By.CSS_SELECTOR, ".el-empty")

    @allure.step("打开收货地址")
    def open(self) -> None:
        super().open(self.URL)

    def get_address_count(self) -> int:
        return self.element_count(self.ADDRESS_ITEM)

    def is_empty(self) -> bool:
        return self.is_displayed(self.EMPTY)

    @allure.step("新增地址: {consignee}, {mobile}")
    def add_address(
        self,
        consignee: str,
        mobile: str,
        province: str = "广东省",
        city: str = "深圳市",
        district: str = "南山区",
        address: str = "科技园路100号",
    ) -> None:
        self.click(self.ADDRESS_ADD_BTN)
        self.wait_seconds(0.3)

        self.type(self.CONSIGNEE_INPUT, consignee)
        self.type(self.MOBILE_INPUT, mobile)
        self.type(self.PROVINCE_INPUT, province)
        self.type(self.CITY_INPUT, city)
        self.type(self.DISTRICT_INPUT, district)
        self.type(self.ADDRESS_INPUT, address)

        self.click(self.SAVE_BTN)

    @allure.step("删除第 {index} 个地址")
    def delete_address(self, index: int = 0) -> None:
        items = self.find_all(self.ADDRESS_ITEM)
        if index < len(items):
            del_btns = items[index].find_elements(By.XPATH, ".//button[contains(.,'删除')]")
            if del_btns:
                del_btns[0].click()
                self.wait_seconds(0.3)
                self.el_dialog_confirm()

    @allure.step("设置第 {index} 个为默认地址")
    def set_default(self, index: int = 0) -> None:
        items = self.find_all(self.ADDRESS_ITEM)
        if index < len(items):
            default_btns = items[index].find_elements(By.XPATH, ".//button[contains(.,'默认')]")
            if default_btns:
                default_btns[0].click()

    @allure.step("编辑第 {index} 个地址")
    def edit_address(self, index: int = 0, **kwargs) -> None:
        items = self.find_all(self.ADDRESS_ITEM)
        if index < len(items):
            edit_btns = items[index].find_elements(By.XPATH, ".//button[contains(.,'编辑')]")
            if edit_btns:
                edit_btns[0].click()
                self.wait_seconds(0.3)

            if "consignee" in kwargs:
                self.type(self.CONSIGNEE_INPUT, kwargs["consignee"])
            if "mobile" in kwargs:
                self.type(self.MOBILE_INPUT, kwargs["mobile"])
            if "address" in kwargs:
                self.type(self.ADDRESS_INPUT, kwargs["address"])

            self.click(self.SAVE_BTN)
