"""
WebDriver 工厂 — 优先本机驱动，未安装则自动下载。
"""
import os
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

from config.config import (
    BROWSER, HEADLESS, IMPLICIT_WAIT, PAGE_LOAD_WAIT,
    CHROMEDRIVER_PATH, GECKODRIVER_PATH, EDGEDRIVER_PATH,
)

logger = logging.getLogger(__name__)


def create_driver():
    """根据 BROWSER 配置创建 WebDriver 实例。"""
    factories = {"chrome": _create_chrome, "firefox": _create_firefox, "edge": _create_edge}
    if BROWSER not in factories:
        raise ValueError(f"不支持的浏览器: {BROWSER}, 可选: {list(factories.keys())} ")
    driver = factories[BROWSER]()
    driver.implicitly_wait(IMPLICIT_WAIT)
    driver.set_page_load_timeout(PAGE_LOAD_WAIT)
    logger.info("WebDriver 就绪 — %s", BROWSER)
    return driver


def _get_service(local_path, ServiceCls, webdriver_manager_path):
    """获取 Service：本机有则用本地，否则尝试下载，再否则系统 PATH。"""
    if os.path.isfile(local_path):
        logger.info("使用本机驱动: %s", local_path)
        return ServiceCls(executable_path=local_path)
    try:
        mod_name, cls_name = webdriver_manager_path.rsplit(".", 1)
        mod = __import__(mod_name, fromlist=[cls_name])
        path = getattr(mod, cls_name)().install()
        logger.info("自动下载驱动: %s", path)
        return ServiceCls(path)
    except (ImportError, Exception):
        logger.warning("webdriver-manager 不可用，使用系统 PATH")
        return ServiceCls()


def _create_chrome():
    options = ChromeOptions()
    if HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = _get_service(CHROMEDRIVER_PATH, ChromeService, "webdriver_manager.chrome.ChromeDriverManager")
    return webdriver.Chrome(service=service, options=options)


def _create_firefox():
    options = FirefoxOptions()
    if HEADLESS:
        options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    service = _get_service(GECKODRIVER_PATH, FirefoxService, "webdriver_manager.firefox.GeckoDriverManager")
    return webdriver.Firefox(service=service, options=options)


def _create_edge():
    options = EdgeOptions()
    if HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    service = _get_service(EDGEDRIVER_PATH, EdgeService, "webdriver_manager.microsoft.EdgeChromiumDriverManager")
    return webdriver.Edge(service=service, options=options)
