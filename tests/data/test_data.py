"""
动态测试数据生成器

每次运行时生成唯一数据，避免数据库冲突。
"""

import random
import time
import string


def timestamp() -> str:
    """返回毫秒时间戳字符串（14位）。"""
    return str(int(time.time() * 1000))


def random_string(length: int = 6) -> str:
    """返回随机小写字母串。"""
    return "".join(random.choices(string.ascii_lowercase, k=length))


def random_digits(length: int = 8) -> str:
    """返回随机数字串。"""
    return "".join(random.choices(string.digits, k=length))


# ================================================================
# 用户注册数据
# ================================================================

def new_mobile() -> str:
    """
    生成未注册的测试手机号。

    规则：1[3-9]开头（第二位非2），共11位。
    """
    second = str(random.choice([3, 4, 5, 6, 7, 8, 9]))
    tail = random_digits(9)
    return f"1{second}{tail}"


def new_email(username: str = None) -> str:
    """
    生成未注册的测试邮箱。

    格式：xxxx@[126/sina/qq/163].com
    xxxx长度4-16位，字母开头。
    """
    domains = ["126.com", "sina.com", "qq.com", "163.com"]
    name = username or (random_string(4) + random_digits(4))
    return f"{name}@{random.choice(domains)}"


def valid_password() -> str:
    """生成符合规则的密码（6-16位，大小写+数字+符号至少两种组合）。"""
    return "Test@123"


def weak_password() -> str:
    """生成不符合规则的弱密码（纯数字）。"""
    return "123456"


# ================================================================
# 商品测试数据（后台添加用）
# ================================================================

def new_goods_data() -> dict:
    """
    生成新商品数据。

    Returns:
        dict with keys: goods_name, goods_sn, shop_price, market_price,
                        store_count, goods_content
    """
    ts = timestamp()[-8:]
    return {
        "goods_name": f"测试商品_{ts}",
        "goods_sn": f"TESTSN{ts}",
        "shop_price": str(round(random.uniform(10, 5000), 2)),
        "market_price": str(round(random.uniform(20, 6000), 2)),
        "store_count": str(random.randint(1, 999)),
        "goods_content": f"<p>自动化测试添加的商品详情 — {ts}</p>",
    }


# ================================================================
# 收货地址数据
# ================================================================

def new_address_data() -> dict:
    ts = timestamp()[-6:]
    return {
        "consignee": f"测试用户{ts}",
        "mobile": new_mobile(),
        "province": "广东省",
        "city": "深圳市",
        "district": "南山区",
        "address": f"自动化测试路{ts}号",
    }


# ================================================================
# 订单数据
# ================================================================

def new_order_data() -> dict:
    ts = timestamp()[-6:]
    return {
        "pay_name": "alipay",
        "shipping_name": "express",
        "remark": f"自动化测试订单备注_{ts}",
    }

if __name__ == '__main__':
    timestamp()