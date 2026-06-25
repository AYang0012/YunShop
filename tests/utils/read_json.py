"""
读取 data/ 目录下的 JSON 文件，转为 pytest parametrize 所需元组列表。

JSON 格式:
    [
        {"key1": "v1", "key2": "v2"},
        {"key1": "v3", "key2": "v4"}
    ]

返回:
    [("v1", "v2"), ("v3", "v4")]

用法:
    from utils.read_json import read_json

    @pytest.mark.parametrize("username,password", read_json("login_data.json"))
    def test_login(username, password):
        ...
"""

import json
import os

from config.config import DATA_DIR


def read_json(filename: str) -> list:
    file_path = os.path.join(DATA_DIR, filename)
    with open(file_path, mode="r", encoding="utf-8") as f:
        items = json.load(f)
    return [tuple(item.values()) for item in items]
