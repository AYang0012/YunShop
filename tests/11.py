from datetime import datetime
from pathlib import Path

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from config.config import (
    BASE_URL, API_URL, TEST_USER, ADMIN_USER,
    SCREENSHOT_ON_FAILURE, SCREENSHOT_DIR,
    HEADLESS, CHROMEDRIVER_PATH,
)
from utils.logger import get_logger

logger = get_logger("yunshop_test")


def pytest_configure(config):
    """pytest 启动钩子 — 初始化 Allure 环境信息。"""
    allure_dir = Path(config.getoption("--alluredir", default="reports/allure-results"))
    allure_dir.mkdir(parents=True, exist_ok=True)

    env_file = allure_dir / "environment.properties"
    with open(env_file, "w", encoding="utf-8") as f:
        f.write(f"Browser=chrome\n")
        f.write(f"BaseURL={BASE_URL}\n")
        f.write(f"APIRoot={API_URL}\n")
        f.write(f"Timestamp={datetime.now().isoformat()}\n")

    # 确保截图目录存在
    Path(SCREENSHOT_DIR).mkdir(parents=True, exist_ok=True)


def pytest_sessionstart(session):
    logger.info("=" * 60)
    logger.info("云集优选 自动化测试开始")
    logger.info("  前端地址: %s", BASE_URL)
    logger.info("  后端地址: %s", API_URL)
    logger.info("=" * 60)


def pytest_sessionfinish(session, exitstatus):
    logger.info("测试结束，退出码: %d", exitstatus)


@pytest.fixture(scope="function")
def driver():
    """创建 Chrome WebDriver 实例，用例结束后自动关闭。"""
    logger.info("─" * 40)
    logger.info(">>> 创建 Chrome WebDriver 实例")

    options = webdriver.ChromeOptions()
    if HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    service = Service(executable_path=CHROMEDRIVER_PATH)
    drv = webdriver.Chrome(service=service, options=options)
    drv.maximize_window()
    drv.implicitly_wait(10)

    logger.info(">>> WebDriver 已就绪")
    yield drv
    drv.quit()
    logger.info("<<< WebDriver 已关闭")


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="session")
def api_url():
    return API_URL


@pytest.fixture(scope="session")
def test_user():
    return TEST_USER.copy()


@pytest.fixture(scope="session")
def admin_user():
    return ADMIN_USER.copy()


# ============================================================
# 失败自动截图 + Allure 报告增强
# ============================================================
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver_fixture = item.funcargs.get("driver")
        if driver_fixture and SCREENSHOT_ON_FAILURE:
            _attach_screenshot(driver_fixture, item.name)
            _attach_browser_console(driver_fixture)


def _attach_screenshot(drv, test_name):
    try:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = str(Path(SCREENSHOT_DIR) / f"{test_name}_{ts}.png")
        drv.save_screenshot(filepath)
        allure.attach.file(filepath, name=f"失败截图 — {test_name}",
                           attachment_type=allure.attachment_type.PNG)
        logger.info("📸 失败截图已保存: %s", filepath)
    except Exception as e:
        logger.warning("截图失败: %s", e)


def _attach_browser_console(drv):
    try:
        logs = drv.get_log("browser")
        if logs:
            formatted = "\n".join(
                f"[{entry['level']}] {entry['message']}" for entry in logs
            )
            allure.attach(formatted, name="浏览器控制台日志",
                          attachment_type=allure.attachment_type.TEXT)
    except Exception:
        pass
