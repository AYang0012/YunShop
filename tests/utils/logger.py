"""
测试日志工具

提供统一的日志记录器，测试用例通过 `logger` fixture 使用。
"""

import logging
import sys
from pathlib import Path

from utils.config import PROJECT_ROOT

LOG_DIR = PROJECT_ROOT / "tests" / "reports" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)


def get_logger(name: str = "yunshop_test") -> logging.Logger:
    """
    获取配置好的 logger 实例。

    Args:
        name: 日志记录器名称

    Returns:
        配置了控制台 + 文件双输出的 Logger
    """
    logger = logging.getLogger(name)

    # 避免重复添加 handler
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    # 格式
    fmt = logging.Formatter(
        "%(asctime)s [%(levelname)-7s] %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # 控制台 handler
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    console.setFormatter(fmt)
    logger.addHandler(console)

    # 文件 handler（每次运行追加）
    file_handler = logging.FileHandler(LOG_DIR / "test_run.log", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(fmt)
    logger.addHandler(file_handler)

    return logger
