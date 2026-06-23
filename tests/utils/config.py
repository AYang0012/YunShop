"""
测试框架全局配置

通过环境变量覆盖默认值，支持 CI/CD 灵活配置。
"""

import os
from pathlib import Path

# ── 项目根目录 ──
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# ── 被测应用地址 ──
BASE_URL = os.getenv("YUNSHOP_BASE_URL", "http://localhost:3000")
API_URL  = os.getenv("YUNSHOP_API_URL",  "http://localhost:8080/api")

# ── 浏览器配置 ──
BROWSER = os.getenv("YUNSHOP_BROWSER", "chrome").lower()  # chrome | firefox | edge
HEADLESS = os.getenv("YUNSHOP_HEADLESS", "false").lower() == "true"

# ── 超时时间（秒） ──
IMPLICIT_WAIT  = int(os.getenv("YUNSHOP_IMPLICIT_WAIT",  "10"))
EXPLICIT_WAIT  = int(os.getenv("YUNSHOP_EXPLICIT_WAIT",  "15"))
PAGE_LOAD_WAIT = int(os.getenv("YUNSHOP_PAGE_LOAD_WAIT", "30"))

# ── 测试账号 ──
TEST_USER = {
    "mobile":   os.getenv("YUNSHOP_TEST_MOBILE",   "13800138000"),
    "password": os.getenv("YUNSHOP_TEST_PASSWORD", "Test@123"),
    "email":    os.getenv("YUNSHOP_TEST_EMAIL",    "test@163.com"),
}

ADMIN_USER = {
    "username": os.getenv("YUNSHOP_ADMIN_USERNAME", "admin"),
    "password": os.getenv("YUNSHOP_ADMIN_PASSWORD", "admin123"),
}

# ── 截图 & 报告 ──
SCREENSHOT_ON_FAILURE = os.getenv("YUNSHOP_SCREENSHOT", "true").lower() == "true"
SCREENSHOT_DIR = PROJECT_ROOT / "tests" / "reports" / "screenshots"
ALLURE_RESULTS_DIR = PROJECT_ROOT / "tests" / "reports" / "allure-results"

# ── 确保目录存在 ──
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
ALLURE_RESULTS_DIR.mkdir(parents=True, exist_ok=True)
