"""
WebDriver 工厂

支持 Chrome / Firefox / Edge，自动管理驱动版本（通过 webdriver-manager）。
"""

import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

from utils.config import BROWSER, HEADLESS, IMPLICIT_WAIT, PAGE_LOAD_WAIT

logger = logging.getLogger(__name__)


def create_driver() -> webdriver.Remote:
    """
    根据配置创建 WebDriver 实例。

    Returns:
        配置好的 WebDriver 实例
    """
    driver_factories = {
        "chrome":  _create_chrome,
        "firefox": _create_firefox,
        "edge":    _create_edge,
    }

    factory = driver_factories.get(BROWSER)
    if factory is None:
        raise ValueError(
            f"不支持的浏览器类型: {BROWSER}，可选: {list(driver_factories.keys())}"
        )

    driver = factory()
    _configure_timeouts(driver)
    logger.info("WebDriver 初始化完成 — 浏览器: %s, 无头模式: %s", BROWSER, HEADLESS)
    return driver


def _create_chrome() -> webdriver.Chrome:
    options = ChromeOptions()
    if HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    try:
        from webdriver_manager.chrome import ChromeDriverManager
        service = ChromeService(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)
    except ImportError:
        logger.warning("webdriver-manager 未安装，使用系统 PATH 中的 ChromeDriver")
        return webdriver.Chrome(options=options)


def _create_firefox() -> webdriver.Firefox:
    options = FirefoxOptions()
    if HEADLESS:
        options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")

    try:
        from webdriver_manager.firefox import GeckoDriverManager
        service = FirefoxService(GeckoDriverManager().install())
        return webdriver.Firefox(service=service, options=options)
    except ImportError:
        logger.warning("webdriver-manager 未安装，使用系统 PATH 中的 GeckoDriver")
        return webdriver.Firefox(options=options)


def _create_edge() -> webdriver.Edge:
    options = EdgeOptions()
    if HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")

    try:
        from webdriver_manager.microsoft import EdgeChromiumDriverManager
        service = EdgeService(EdgeChromiumDriverManager().install())
        return webdriver.Edge(service=service, options=options)
    except ImportError:
        logger.warning("webdriver-manager 未安装，使用系统 PATH 中的 EdgeDriver")
        return webdriver.Edge(options=options)


def _configure_timeouts(driver: webdriver.Remote) -> None:
    """配置全局超时。"""
    driver.implicitly_wait(IMPLICIT_WAIT)
    driver.set_page_load_timeout(PAGE_LOAD_WAIT)
