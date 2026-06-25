"""
BasePage — 所有 Page Object 的基类

封装通用 Selenium 操作：查找、点击、输入、等待、滚动、截图等。
子类继承后只需定义页面元素定位器 + 业务方法。

参照 BaseProject common/base.py 的简洁设计哲学，保留核心方法约 25 个。
"""

import logging
import time
from typing import List, Tuple

import allure
from selenium import webdriver
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select

from config.config import EXPLICIT_WAIT

logger = logging.getLogger(__name__)


class BasePage:
    """
    页面对象基类。

    子类用法:
        class LoginPage(BasePage):
            URL = f"{BASE_URL}/login"

            USERNAME_INPUT = (By.CSS_SELECTOR, "input[placeholder*='手机号']")
            PASSWORD_INPUT = (By.CSS_SELECTOR, "input[type='password']")

            def login(self, username, password):
                self.type(self.USERNAME_INPUT, username)
                self.type(self.PASSWORD_INPUT, password)
                self.click(self.SUBMIT_BTN)
    """

    def __init__(self, driver: webdriver.Remote, timeout: int = None):
        """
        Args:
            driver: WebDriver 实例
            timeout: 显式等待超时（秒），默认读取 config.EXPLICIT_WAIT
        """
        self.driver = driver
        self.timeout = timeout or EXPLICIT_WAIT
        self.wait = WebDriverWait(driver, self.timeout)

    # ================================================================
    # 页面导航
    # ================================================================

    @allure.step("打开页面: {url}")
    def open(self, url: str) -> None:
        """导航到指定 URL。"""
        self.driver.get(url)
        logger.info("已打开: %s", url)

    def refresh(self) -> None:
        """刷新当前页面。"""
        self.driver.refresh()

    @property
    def current_url(self) -> str:
        return self.driver.current_url

    @property
    def page_title(self) -> str:
        return self.driver.title

    # ================================================================
    # 元素查找
    # ================================================================

    def find(
        self,
        locator: Tuple[By, str],
        timeout: int = None,
    ) -> WebElement:
        """
        查找单个可见元素（显式等待）。

        Args:
            locator: (By.CSS_SELECTOR, ".class") 或 (By.XPATH, "//div")
            timeout: 超时秒数，默认使用实例 timeout

        Returns:
            WebElement 实例

        Raises:
            TimeoutException: 超时未找到
        """
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        return wait.until(EC.visibility_of_element_located(locator))

    def find_present(
        self,
        locator: Tuple[By, str],
        timeout: int = None,
    ) -> WebElement:
        """查找单个元素（仅需存在于 DOM，不要求可见）。"""
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        return wait.until(EC.presence_of_element_located(locator))

    def find_all(
        self,
        locator: Tuple[By, str],
        timeout: int = None,
    ) -> List[WebElement]:
        """查找所有可见元素。"""
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        return wait.until(EC.visibility_of_all_elements_located(locator))

    def find_all_present(
        self,
        locator: Tuple[By, str],
        timeout: int = None,
    ) -> List[WebElement]:
        """查找所有存在于 DOM 的元素。"""
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        return wait.until(EC.presence_of_all_elements_located(locator))

    def is_displayed(self, locator: Tuple[By, str], timeout: int = 3) -> bool:
        """判断元素是否可见（短超时，不抛异常）。"""
        try:
            return self.find(locator, timeout=timeout).is_displayed()
        except (TimeoutException, NoSuchElementException):
            return False

    def is_present(self, locator: Tuple[By, str], timeout: int = 3) -> bool:
        """判断元素是否存在于 DOM。"""
        try:
            self.find_present(locator, timeout=timeout)
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def element_count(self, locator: Tuple[By, str]) -> int:
        """获取匹配元素数量。"""
        return len(self.driver.find_elements(*locator))

    # ================================================================
    # 元素操作
    # ================================================================

    @allure.step("点击: {locator[1]}")
    def click(self, locator: Tuple[By, str], timeout: int = None) -> None:
        """点击元素（内置重试处理 click intercepted）。"""
        el = self.find(locator, timeout=timeout)
        try:
            el.click()
        except ElementClickInterceptedException:
            self._scroll_to(el)
            el.click()

    def click_js(self, locator: Tuple[By, str]) -> None:
        """通过 JavaScript 强制点击（绕过可见性检查）。"""
        el = self.find(locator)
        self.driver.execute_script("arguments[0].click();", el)

    @allure.step("输入: {locator[1]} ← …")
    def type(
        self,
        locator: Tuple[By, str],
        text: str,
        clear_first: bool = True,
    ) -> None:
        """
        向输入框输入文本。

        Args:
            locator: 元素定位器
            text: 要输入的文本
            clear_first: 是否先清空已有内容
        """
        el = self.find(locator)
        if clear_first:
            el.clear()
        el.send_keys(text)

    # ================================================================
    # 内容读取
    # ================================================================

    def get_text(self, locator: Tuple[By, str]) -> str:
        """获取元素文本内容。"""
        return self.find(locator).text

    def get_attribute(self, locator: Tuple[By, str], attr: str) -> str:
        """获取元素属性值。"""
        return self.find(locator).get_attribute(attr)

    def get_value(self, locator: Tuple[By, str]) -> str:
        """获取输入框当前值。"""
        return self.get_attribute(locator, "value")

    # ================================================================
    # 等待 & 判断
    # ================================================================

    def wait_for_clickable(
        self,
        locator: Tuple[By, str],
        timeout: int = None,
    ) -> WebElement:
        """等待元素可点击。"""
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        return wait.until(EC.element_to_be_clickable(locator))

    def wait_for_invisible(
        self,
        locator: Tuple[By, str],
        timeout: int = None,
    ) -> bool:
        """等待元素不可见（常用于等待 loading 消失）。"""
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        return wait.until(EC.invisibility_of_element_located(locator))

    def wait_for_text(
        self,
        locator: Tuple[By, str],
        text: str,
        timeout: int = None,
    ) -> bool:
        """等待元素包含指定文本。"""
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        return wait.until(EC.text_to_be_present_in_element(locator, text))

    def wait_for_url_contains(self, fragment: str, timeout: int = None) -> bool:
        """等待 URL 包含指定字符串。"""
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        return wait.until(EC.url_contains(fragment))

    def _pause(self, seconds: float = 0.5) -> None:
        """
        短暂固定等待，仅用于过渡动画等显式等待无法覆盖的极少数场景。

        **已弃用** — 优先使用 wait_for_* 系列方法。
        """
        time.sleep(seconds)

    # ================================================================
    # 滚动 & 鼠标
    # ================================================================

    def _scroll_to(self, element: WebElement) -> None:
        """滚动到元素可见位置。"""
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', behavior: 'instant'});",
            element,
        )

    def scroll_to(self, locator: Tuple[By, str]) -> None:
        """滚动到指定元素。"""
        el = self.find(locator)
        self._scroll_to(el)

    def scroll_to_bottom(self) -> None:
        """滚动到页面底部。"""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def scroll_to_top(self) -> None:
        """滚动到页面顶部。"""
        self.driver.execute_script("window.scrollTo(0, 0);")

    def hover(self, locator: Tuple[By, str]) -> None:
        """鼠标悬停到指定元素。"""
        el = self.find(locator)
        ActionChains(self.driver).move_to_element(el).perform()

    # ================================================================
    # 下拉选择 & 复选框
    # ================================================================

    def select_by_text(
        self, locator: Tuple[By, str], text: str
    ) -> None:
        """原生 <select> 按可见文本选择。"""
        el = self.find(locator)
        Select(el).select_by_visible_text(text)

    def select_by_value(
        self, locator: Tuple[By, str], value: str
    ) -> None:
        """原生 <select> 按 value 选择。"""
        el = self.find(locator)
        Select(el).select_by_value(value)

    def checkbox_check(
        self, locator: Tuple[By, str], check: bool = True
    ) -> None:
        """
        勾选/取消勾选复选框。

        Args:
            locator: 复选框定位器
            check: True=勾选, False=取消勾选
        """
        el = self.find(locator)
        if el.is_selected() != check:
            el.click()

    # ================================================================
    # Alert / 弹窗
    # ================================================================

    def accept_alert(self, timeout: int = 5) -> str:
        """接受 alert 弹窗，返回弹窗文本。"""
        wait = WebDriverWait(self.driver, timeout)
        wait.until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        text = alert.text
        alert.accept()
        return text

    def dismiss_alert(self, timeout: int = 5) -> str:
        """取消 alert 弹窗。"""
        wait = WebDriverWait(self.driver, timeout)
        wait.until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        text = alert.text
        alert.dismiss()
        return text

    # ================================================================
    # 窗口 / Frame / Tab
    # ================================================================

    def switch_to_new_window(self) -> None:
        """切换到最新打开的窗口。"""
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[-1])

    def switch_to_main_window(self) -> None:
        """切换回主窗口。"""
        self.driver.switch_to.window(self.driver.window_handles[0])

    def switch_to_frame(self, locator: Tuple[By, str]) -> None:
        """切换到 iframe。"""
        frame = self.find(locator)
        self.driver.switch_to.frame(frame)

    def switch_to_default_content(self) -> None:
        """从 iframe 切回主文档。"""
        self.driver.switch_to.default_content()

    # ================================================================
    # 截图
    # ================================================================

    def screenshot(self, filename: str = None) -> str:
        """
        保存截图。

        Args:
            filename: 文件名（不含路径），默认使用时间戳

        Returns:
            截图文件完整路径
        """
        from datetime import datetime
        import os
        from config.config import SCREENSHOT_DIR

        if filename is None:
            filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

        filepath = os.path.join(SCREENSHOT_DIR, filename)
        self.driver.save_screenshot(filepath)
        logger.info("📸 截图已保存: %s", filepath)
        return filepath

    # ================================================================
    # Element Plus 组件专用
    # ================================================================

    def el_select_option(
        self,
        select_placeholder: str,
        option_text: str,
    ) -> None:
        """
        Element Plus 下拉选择：点击触发 → 等待选项出现 → 点击选项。

        Args:
            select_placeholder: 下拉框的 placeholder 文本
            option_text: 要选择的选项文本
        """
        trigger = (
            By.XPATH,
            f"//input[@placeholder='{select_placeholder}']",
        )
        self.click(trigger)

        option = (
            By.XPATH,
            f"//div[contains(@class,'el-select-dropdown')]//li[contains(@class,'el-select-dropdown__item')]/span[text()='{option_text}']",
        )
        self.click(option)

    def el_message_should_contain(self, text: str) -> bool:
        """
        验证 Element Plus Message 提示内容。

        Args:
            text: 期望包含的文本

        Returns:
            True 如果提示包含指定文本
        """
        locator = (
            By.CSS_SELECTOR,
            ".el-message .el-message__content, .el-message__content",
        )
        try:
            actual = self.get_text(locator)
            return text in actual
        except TimeoutException:
            return False

    def el_dialog_confirm(self) -> None:
        """点击 Element Plus Dialog 确认按钮。"""
        btn = (By.CSS_SELECTOR, ".el-dialog .el-button--primary, .el-message-box__btns .el-button--primary")
        self.click(btn)

    def el_dialog_cancel(self) -> None:
        """点击 Element Plus Dialog 取消按钮。"""
        btn = (By.CSS_SELECTOR, ".el-dialog .el-button:not(.el-button--primary), .el-message-box__btns .el-button:not(.el-button--primary)")
        self.click(btn)
