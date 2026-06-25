#!/usr/bin/env python
"""
云集优选 自动化测试 — 便捷运行入口

用法:
    python run_tests.py              # 运行全部测试
    python run_tests.py smoke        # 运行冒烟测试
    python run_tests.py regression   # 运行回归测试
    python run_tests.py front        # 只运行前台测试
    python run_tests.py admin        # 只运行后台测试
    python run_tests.py p0           # 只运行 P0 级别用例
    python run_tests.py p1           # 只运行 P1 级别用例
"""

import subprocess
import sys

TARGETS = {
    "smoke":      "-m smoke",
    "regression": "-m regression",
    "front":      "cases/front",
    "admin":      "cases/admin",
    "p0":         "-m p0",
    "p1":         "-m p1",
    "p2":         "-m p2",
    "all":        "cases",
}


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "all"
    mark = TARGETS.get(target, target)

    cmd = (
        f"pytest {mark} -v --tb=short "
        f"--alluredir=reports/allure-results --clean-alluredir"
    )
    print(f">>> 运行命令: {cmd}")
    subprocess.run(cmd, shell=True, cwd="G:/TestProject/tests")


if __name__ == "__main__":
    main()
