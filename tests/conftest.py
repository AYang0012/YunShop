"""
项目根级 pytest 配置

提供全局 fixture：driver、base_url、logger、test_user 等。
集成 Allure 报告：失败自动截图 + 浏览器日志。
"""

import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Generator

import allure
import pytest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from utils.config import (
    BASE_URL, API_URL, TEST_USER, ADMIN_USER,
    EXPLICIT_WAIT, SCREENSHOT_ON_FAILURE, SCREENSHOT_DIR,
)
from utils.driver_factory import create_driver
from utils.logger import get_logger


# ============================================================
# 全局 Logger
# ============================================================
logger = get_logger("yunshop_test")


def pytest_configure(config):
    """pytest 启动钩子 — 初始化 Allure 环境信息。"""
    allure_dir = Path(config.getoption("--alluredir", default="reports/allure-results"))
    allure_dir.mkdir(parents=True, exist_ok=True)

    env_file = allure_dir / "environment.properties"
    with open(env_file, "w", encoding="utf-8") as f:
        f.write(f"Browser={__import__('utils.config', fromlist=['BROWSER']).BROWSER}\n")
        f.write(f"BaseURL={BASE_URL}\n")
        f.write(f"APIRoot={API_URL}\n")
        f.write(f"Timestamp={datetime.now().isoformat()}\n")


def pytest_sessionstart(session):
    logger.info("=" * 60)
    logger.info("云集优选 自动化测试开始")
    logger.info("  前端地址: %s", BASE_URL)
    logger.info("  后端地址: %s", API_URL)
    logger.info("=" * 60)


def pytest_sessionfinish(session, exitstatus):
    logger.info("测试结束，退出码: %d", exitstatus)


# ============================================================
# Driver Fixture（function 级别 — 每个用例独立浏览器实例）
# ============================================================
@pytest.fixture(scope="function")
def driver() -> Generator[webdriver.Remote, None, None]:
    """
    创建并管理 WebDriver 生命周期。

    用法:
        def test_example(driver):
            driver.get("http://localhost:3000")
            assert "云集优选" in driver.title
    """
    logger.info("─" * 40)
    logger.info(">>> 创建 WebDriver 实例")

    drv = None
    try:
        drv = create_driver()
        logger.info(">>> WebDriver 已就绪")
        yield drv
    except WebDriverException as e:
        logger.error(">>> WebDriver 异常: %s", e)
        raise
    finally:
        if drv:
            try:
                drv.quit()
                logger.info("<<< WebDriver 已关闭")
            except Exception as e:
                logger.warning("<<< 关闭 WebDriver 时出错: %s", e)


# ============================================================
# 应用级 Fixture
# ============================================================
@pytest.fixture(scope="session")
def base_url() -> str:
    """被测前端根地址。"""
    return BASE_URL


@pytest.fixture(scope="session")
def api_url() -> str:
    """被测 API 根地址。"""
    return API_URL


@pytest.fixture(scope="session")
def test_user() -> dict:
    """标准测试用户凭证。"""
    return TEST_USER.copy()


@pytest.fixture(scope="session")
def admin_user() -> dict:
    """后台管理员凭证。"""
    return ADMIN_USER.copy()


# ============================================================
# 失败自动截图 + Allure 报告增强
# ============================================================
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    测试失败时自动截图，附加到 Allure 报告。
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver_fixture = item.funcargs.get("driver")
        if driver_fixture and SCREENSHOT_ON_FAILURE:
            _attach_screenshot(driver_fixture, item.name)
            _attach_browser_console(driver_fixture)


def _attach_screenshot(drv: webdriver.Remote, test_name: str) -> None:
    """截图并附加到 Allure。"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{test_name}_{timestamp}.png"
        filepath = SCREENSHOT_DIR / filename
        drv.save_screenshot(str(filepath))

        allure.attach.file(
            str(filepath),
            name=f"失败截图 — {test_name}",
            attachment_type=allure.attachment_type.PNG,
        )
        logger.info("📸 失败截图已保存: %s", filepath)
    except Exception as e:
        logger.warning("截图失败: %s", e)


def _attach_browser_console(drv: webdriver.Remote) -> None:
    """获取浏览器控制台日志并附加到 Allure（仅 Chrome）。"""
    try:
        logs = drv.get_log("browser")
        if logs:
            formatted = "\n".join(
                f"[{entry['level']}] {entry['message']}" for entry in logs
            )
            allure.attach(
                formatted,
                name="浏览器控制台日志",
                attachment_type=allure.attachment_type.TEXT,
            )
    except Exception:
        pass  # 非 Chrome 或 log 不可用
