# 项目配置相关的文件
import os
from faker import Faker

# 获取项目路径
PATH = os.path.dirname(__file__)

# 项目的地址
BASE_URL = "http://localhost:3000"
API_URL = "http://localhost:8080/api"

# 浏览器配置
BROWSER = "chrome"
HEADLESS = False
CHROMEDRIVER_PATH = ""   # 留空则自动通过 webdriver-manager 下载
GECKODRIVER_PATH = ""    # 留空则自动通过 webdriver-manager 下载
EDGEDRIVER_PATH = ""     # 留空则自动通过 webdriver-manager 下载

# 超时时间（秒）
IMPLICIT_WAIT = 10
EXPLICIT_WAIT = 15
PAGE_LOAD_WAIT = 30

# 测试账号
TEST_USER = {
    "mobile": "13800138000",
    "password": "Test@123",
    "email": "test@163.com",
}

ADMIN_USER = {
    "username": "admin",
    "password": "admin123",
}

# 路径 : 截图 & 报告 & 日志 & 测试数据
SCREENSHOT_ON_FAILURE = True
SCREENSHOT_DIR = os.path.join(PATH, "..", "reports", "screenshots")
ALLURE_RESULTS_DIR = os.path.join(PATH, "..", "reports", "allure-results")
LOG_DIR = os.path.join(PATH, "..", "reports", "logs")
DATA_DIR = os.path.join(PATH, "..", "data")

# 人的信息  ──使用 Faker 对象生成
fk = Faker(locale="zh_CN")
NAME = fk.name()
PHONE = fk.phone_number()
CARD = fk.ssn()

# ── URL 片段 ──
URL_HOME = "/"
URL_LOGIN = "/login"
URL_REGISTER = "/register"
URL_GOODS_LIST = "/goods/list"
URL_GOODS_DETAIL = "/goods/detail/"
URL_CART = "/cart"
URL_ORDER_CONFIRM = "/order/confirm"
URL_ORDER_DETAIL = "/order/detail/"
URL_USER = "/user"
URL_USER_ORDERS = "/user/orders"
URL_USER_ADDRESS = "/user/address"
URL_USER_PROFILE = "/user/profile"
URL_USER_PASSWORD = "/user/password"
URL_ADMIN_LOGIN = "/admin/login"
URL_ADMIN = "/admin"
URL_ADMIN_GOODS = "/admin/goods"
URL_ADMIN_GOODS_EDIT = "/admin/goods/edit"
URL_ADMIN_CATEGORY = "/admin/category"
URL_ADMIN_ORDER = "/admin/order"
URL_ADMIN_USER = "/admin/user"

# ── 页面标题 ──
TITLE_LOGIN_PAGE = "登录云集优选"
TITLE_REGISTER_PAGE = "注册云集优选"
TITLE_ADMIN_LOGIN_PAGE = "云集优选 · 后台管理"
LOGO_TEXT = "云集优选"

# ── 成功提示 ──
MSG_LOGIN_SUCCESS = "登录成功"
MSG_REGISTER_SUCCESS = "注册成功"
MSG_LOGOUT_SUCCESS = "已安全退出"
MSG_ADMIN_LOGIN_OK = "登录成功"
MSG_ADD_TO_CART_OK = "已加入购物车"
MSG_ORDER_SUBMIT_OK = "下单成功"
MSG_ORDER_PAID_OK = "支付成功"
MSG_ORDER_CANCELLED_OK = "已取消"
MSG_ORDER_RECEIVED_OK = "已收货"
MSG_ADDRESS_SAVED = "保存成功"
MSG_PASSWORD_CHANGED = "密码修改成功"
MSG_PROFILE_UPDATED = "更新成功"
MSG_DELETED = "已删除"

# ── 错误提示 ──
MSG_LOGIN_FAIL = "用户名或密码错误"
MSG_EMPTY_CART = "购物车还没有任何商品，马上去购物"
MSG_NO_GOODS = "暂无商品"

# ── Element Plus 类名 ──
CLASS_EL_MESSAGE = "el-message"
CLASS_EL_MESSAGE_BOX = "el-message-box"
CLASS_EL_EMPTY = "el-empty"
CLASS_EL_PAGINATION = "el-pagination"
CLASS_EL_FORM_ERROR = "el-form-item__error"
