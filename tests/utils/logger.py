"""
测试日志工具

提供统一的日志记录器，测试用例通过 logger fixture 使用。
参照 BaseProject 的 GetLog 类，使用 TimedRotatingFileHandler 按天归档。
"""

import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler

from config.config import LOG_DIR


def get_logger(name: str = "yunshop_test") -> logging.Logger:
    """
    获取配置好的 logger 实例。

    Args:
        name: 日志记录器名称

    Returns:
        配置了控制台 + 每日归档文件双输出的 Logger
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

    # 控制台 handler（INFO 级别）
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    console.setFormatter(fmt)
    logger.addHandler(console)

    # 文件 handler — 每日归档，保留最近 7 天
    file_handler = TimedRotatingFileHandler(
        filename=os.path.join(LOG_DIR, "test_run.log"),
        when="midnight",
        interval=1,
        backupCount=7,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(fmt)
    logger.addHandler(file_handler)

    return logger
