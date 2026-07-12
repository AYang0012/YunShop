# 自动化测试框架教程 — pytest + Selenium + Page Object + Allure

> 基于云集优选（YunShop）电商平台的完整自动化测试框架  
> 75 条用例 · 19 个 Page Object · 45 个 Python 文件

---

## 目录

1. [框架架构总览](#1-框架架构总览)
2. [pytest 核心机制](#2-pytest-核心机制)
3. [Selenium WebDriver 深度应用](#3-selenium-webdriver-深度应用)
4. [Page Object 设计模式](#4-page-object-设计模式)
5. [Allure 测试报告](#5-allure-测试报告)
6. [测试配置管理](#6-测试配置管理)
7. [数据驱动与测试数据管理](#7-数据驱动与测试数据管理)
8. [WebDriver 工厂模式](#8-webdriver-工厂模式)
9. [日志系统](#9-日志系统)
10. [Element Plus 组件测试技巧](#10-element-plus-组件测试技巧)
11. [实战：编写一条完整用例](#11-实战编写一条完整用例)

---

## 1. 框架架构总览

### 1.1 技术栈

| 层级 | 技术 | 版本 | 用途 |
|------|------|------|------|
| 测试框架 | pytest | 9.0.3 | 用例执行、fixture、标记 |
| 浏览器驱动 | Selenium | 4.44.0 | 浏览器自动化 |
| 设计模式 | Page Object | — | 页面对象封装 |
| 报告框架 | Allure | 2.16.0 | 可视化测试报告 |
| 驱动管理 | webdriver-manager | 4.0.0 | 自动下载匹配的驱动 |
| 配置管理 | 环境变量 | — | 12 个可覆盖配置项 |

### 1.2 分层架构

```
tests/
├── conftest.py          ← 第1层：全局 pytest 配置 + driver fixture + 失败截图钩子
├── pytest.ini           ← 第1层：pytest 配置 + 6个自定义标记
├── utils/               ← 第2层：工具层（config / driver_factory / logger）
├── pages/               ← 第3层：页面对象层（1个 BasePage + 19个 Page Object）
├── cases/               ← 第4层：测试用例层（10个模块 + 用例 conftest.py）
│   └── conftest.py      ← 页面对象 fixtures + 复合登录 fixtures
└── data/                ← 第5层：数据层（常量 + 动态数据生成器）
```

**分层原则**：每一层只依赖下一层，不允许跨层调用。

```
测试用例 → Page Object → BasePage → WebDriver
   ↓           ↓            ↓
 data/     utils/       utils/config
```

### 1.3 设计模式一览

| 模式 | 文件 | 体现 |
|------|------|------|
| Page Object | `pages/base_page.py` | 封装页面元素与操作 |
| 工厂模式 | `utils/driver_factory.py` | 多浏览器统一创建 |
| 模板方法 | `BasePage.find()` / `BasePage.click()` | 子类定义定位器，基类提供操作 |
| 依赖注入 | `cases/conftest.py` | pytest fixture 自动注入 Page Object |
| 装饰器模式 | `@allure.step` | 为方法增加 Allure 步骤报告 |
| 策略模式 | 定位器元组 `(By, str)` | 不同定位策略统一接口 |

---

## 2. pytest 核心机制

### 2.1 Fixture — 依赖注入系统

Fixture 是 pytest 最重要的概念，用于"准备测试所需资源"。框架中使用了两个 scope 的 fixture：

```python
# tests/conftest.py

# 每个测试函数独立创建一个浏览器实例
@pytest.fixture(scope="function")
def driver() -> Generator[webdriver.Remote, None, None]:
    """function 级别：每个用例独立浏览器，用完后关闭"""
    drv = create_driver()
    yield drv          # yield 之前 = setup, 之后 = teardown
    drv.quit()         # 每个用例结束自动执行


# 整个测试 session 共享
@pytest.fixture(scope="session")
def base_url() -> str:
    """session 级别：全局只计算一次"""
    return BASE_URL
```

**Fixture Scope 对比：**

| Scope | 生命周期 | 适用场景 | 示例 |
|-------|---------|---------|------|
| `function` | 每个测试函数 | 浏览器实例 | `driver` |
| `class` | 每个测试类 | 共享数据库连接 | — |
| `module` | 每个 .py 文件 | 批量数据准备 | — |
| `session` | 整个测试运行 | 全局配置 | `base_url`、`test_user` |

**Fixture 链式依赖：**

```python
# tests/cases/conftest.py

@pytest.fixture
def login_page(driver):      # ← 依赖 driver fixture
    return LoginPage(driver)

@pytest.fixture
def logged_in(driver, login_page, test_user):  # ← 同时依赖三个 fixture
    """组合 fixture：自动完成登录"""
    login_page.open()
    login_page.login(test_user["mobile"], test_user["password"])
    return test_user
```

### 2.2 自定义 Markers（标记系统）

在 `pytest.ini` 中注册标记，然后用于筛选、跳过、分类：

```ini
# tests/pytest.ini
markers =
    smoke: 冒烟测试（核心流程快速验证）
    regression: 回归测试（完整功能验证）
    front: 前台功能测试
    admin: 后台功能测试
    login_required: 需要登录态的测试
    p0: P0 级用例 — 核心功能
    p1: P1 级用例 — 重要功能
    p2: P2 级用例 — 边缘场景
```

**使用方式：**

```python
@pytest.mark.smoke
@pytest.mark.p0
def test_login_success(self, login_page, test_user):
    ...
```

**运行筛选：**

```bash
pytest -m smoke                  # 只跑冒烟测试
pytest -m "front and p0"         # 前台 P0 级
pytest -m "not login_required"   # 跳过需要登录的
pytest -m "p0 or p1"             # P0 或 P1
```

### 2.3 参数化（parametrize）

一条测试函数，多组数据自动映射：

```python
# tests/cases/front/test_order.py

@pytest.mark.parametrize("status,tab_name", [
    ("all",       "全部"),
    ("PENDING",   "待付款"),
    ("PAID",      "待发货"),
    ("SHIPPED",   "待收货"),
    ("COMPLETED", "已完成"),
    ("CANCELLED", "已取消"),
])
def test_filter_by_status(self, user_orders_page, logged_in, status, tab_name):
    """一条用例覆盖 6 个订单状态 Tab"""
    user_orders_page.open()
    user_orders_page.filter_by_status(status)
    assert "/user/orders" in user_orders_page.current_url
```

参数化的两个核心参数：
- 第1个参数：`"status,tab_name"` — 形参名，逗号分隔
- 第2个参数：`[(值1,值2), ...]` — 每组参数为一个元组

**更精简的写法（仅一个参数时）：**

```python
@pytest.mark.parametrize("field", ["username", "password", "captcha"])
def test_login_empty_field_validation(self, login_page, test_user, field):
    """一条用例覆盖 3 个空字段场景"""
```

### 2.4 pytest 钩子（Hooks）

框架使用了三个关键钩子：

```python
# tests/conftest.py

def pytest_configure(config):
    """① 启动时：写入 Allure 环境信息"""
    allure_dir = Path(config.getoption("--alluredir"))
    env_file = allure_dir / "environment.properties"
    with open(env_file, "w") as f:
        f.write(f"Browser={BROWSER}\n")
        f.write(f"BaseURL={BASE_URL}\n")


def pytest_sessionstart(session):
    """② 开始：打印启动信息"""
    logger.info("云集优选 自动化测试开始")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """③ 每个用例结束：失败时自动截图"""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        _attach_screenshot(item.funcargs["driver"], item.name)
```

**`report.when` 的三个阶段：**

| 值 | 阶段 | 说明 |
|----|------|------|
| `"setup"` | fixture 准备 | driver 创建等 |
| `"call"` | 测试执行 | 实际的 test_xxx 函数 |
| `"teardown"` | 清理 | driver.quit() 等 |

### 2.5 conftest.py 的层级作用

```
tests/conftest.py          ← 根级：所有用例都能用
tests/cases/conftest.py    ← cases 级：cases/ 下的用例才能用
tests/cases/front/         ← 可以继续更深层（本项目未使用）
```

pytest 会自动合并所有 `conftest.py`，内层的可以 `@pytest.fixture` 覆盖外层同名 fixture。

---

## 3. Selenium WebDriver 深度应用

### 3.1 元素定位 — 8 种 By 策略

```python
from selenium.webdriver.common.by import By

# 项目中主要使用两种：
USERNAME_INPUT = (By.CSS_SELECTOR, "input[placeholder*='手机号']")
SUBMIT_BTN     = (By.XPATH, "//button[contains(.,'登录')]")

# 全部 8 种定位方式：
(By.ID, "myId")                  # ← 最快，唯一
(By.CLASS_NAME, "my-class")      # ← 类名
(By.NAME, "myName")              # ← name 属性
(By.TAG_NAME, "input")           # ← 标签名（通常很宽泛）
(By.LINK_TEXT, "立即注册")       # ← a 标签的完整文本
(By.PARTIAL_LINK_TEXT, "注册")   # ← a 标签的部分文本
(By.CSS_SELECTOR, ".class #id")  # ← 灵活强大（推荐）
(By.XPATH, "//div[@attr='val']") # ← 最灵活但最慢
```

**本项目选择策略的优先级：**

```
1. CSS Selector  → 优先使用，性能好
2. XPath 文本定位 → 当需要通过文字定位时使用
3. placeholder 属性 → Element Plus 组件特有
```

### 3.2 隐式等待 vs 显式等待 vs 固定等待

```python
# ❌ 不推荐：固定等待（项目中也用了一点，仅在极端场景）
time.sleep(3)

# ⚠️ 隐式等待（全局生效，但有局限性）
driver.implicitly_wait(10)  # 查找元素时最多等10秒

# ✅ 推荐：显式等待（精确、灵活、可组合）
wait = WebDriverWait(driver, 15)
element = wait.until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, ".submit-btn"))
)
```

**BasePage 封装的 10 种显式等待：**

```python
# 可见性
self.find(locator)                         # EC.visibility_of_element_located
self.find_all(locator)                     # EC.visibility_of_all_elements_located

# DOM 存在（不要求可见）
self.find_present(locator)                 # EC.presence_of_element_located
self.find_all_present(locator)             # EC.presence_of_all_elements_located

# 可点击
self.wait_for_clickable(locator)           # EC.element_to_be_clickable

# 不可见（等待 loading 消失）
self.wait_for_invisible(locator)           # EC.invisibility_of_element_located

# 文本判断
self.wait_for_text(locator, "期望文本")    # EC.text_to_be_present_in_element

# URL 判断
self.wait_for_url_contains("/login")       # EC.url_contains

# Alert
self.accept_alert()                        # EC.alert_is_present

# 存在性快速判断（短超时，不抛异常）
self.is_displayed(locator)                 # 3秒内判断，返回 bool
self.is_present(locator)                   # 3秒内判断，返回 bool
```

### 3.3 为什么优先显式等待？

```python
# 场景：登录后等待页面跳转
# ❌ 隐式等待做不到——它只影响 find_element，不影响 URL 判断
# ✅ 显式等待可以等任何条件
self.wait_for_url_contains(URL_HOME, timeout=5)
```

### 3.4 ActionChains — 模拟复杂鼠标操作

```python
from selenium.webdriver.common.action_chains import ActionChains

# 悬停（触发下拉菜单）
def hover(self, locator):
    el = self.find(locator)
    ActionChains(self.driver).move_to_element(el).perform()

# 右键点击
def right_click(self, locator):
    el = self.find(locator)
    ActionChains(self.driver).context_click(el).perform()

# 双击
def double_click(self, locator):
    el = self.find(locator)
    ActionChains(self.driver).double_click(el).perform()

# 拖拽
def drag_and_drop(self, source, target):
    ActionChains(self.driver).drag_and_drop(src, tgt).perform()
```

### 3.5 JavaScript 执行

```python
# JS 强制点击（元素被遮挡时）
self.driver.execute_script("arguments[0].click();", element)

# 滚动到元素
self.driver.execute_script(
    "arguments[0].scrollIntoView({block: 'center'});", element
)

# 滚动到页面底部
self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# 回到顶部
self.driver.execute_script("window.scrollTo(0, 0);")
```

### 3.6 send_keys 发送按键

```python
from selenium.webdriver.common.keys import Keys

# 回车
self.find(input_locator).send_keys(Keys.ENTER)

# Tab
self.find(input_locator).send_keys(Keys.TAB)

# Escape
self.find(input_locator).send_keys(Keys.ESCAPE)
```

---

## 4. Page Object 设计模式

### 4.1 设计哲学

```
Page Object = 元素定位器 (Locators) + 业务方法 (Actions)

一个 Page Object 应该：
  ✅ 封装一个页面的所有元素和操作
  ✅ 对外暴露业务语义的接口（login() 而不是 click_submit()）
  ✅ 不暴露 WebDriver 细节给测试用例
  ❌ 不包含断言（断言属于测试用例层）
```

### 4.2 BasePage 设计

```python
class BasePage:
    def __init__(self, driver, timeout=None):
        self.driver = driver
        self.timeout = timeout or EXPLICIT_WAIT
        self.wait = WebDriverWait(driver, self.timeout)
```

**BasePage 提供的能力（三大类）：**

| 类别 | 方法数量 | 代表方法 |
|------|---------|---------|
| 元素查找 | 8 | `find()`, `find_all()`, `is_displayed()`, `element_count()` |
| 元素操作 | 6 | `click()`, `type()`, `get_text()`, `get_value()` |
| 页面交互 | 16 | `hover()`, `scroll_to()`, `switch_to_frame()`, `accept_alert()` |
| 等待判断 | 6 | `wait_for_clickable()`, `wait_for_invisible()`, `wait_for_url_contains()` |
| Element Plus 专用 | 3 | `el_select_option()`, `el_dialog_confirm()`, `el_message_should_contain()` |

**总计约 50 个开箱即用的方法。**

### 4.3 BasePage 的核心设计技巧

**技巧 1：click 内置拦截重试**

```python
def click(self, locator, timeout=None):
    el = self.find(locator, timeout=timeout)
    try:
        el.click()
    except ElementClickInterceptedException:
        self._scroll_to(el)  # 元素被遮挡 → 先滚动再点
        el.click()
```

**技巧 2：type 支持清空**

```python
def type(self, locator, text, clear_first=True):
    el = self.find(locator)
    if clear_first:
        el.clear()
    el.send_keys(text)
```

**技巧 3：checkbox 状态感知**

```python
def checkbox_check(self, locator, check=True):
    el = self.find(locator)
    if el.is_selected() != check:   # 只在状态不对时才点击
        el.click()
```

### 4.4 页面对象实现模板

```python
from pages.base_page import BasePage

class LoginPage(BasePage):
    # ── 1. 定义 URL ──
    URL = f"{BASE_URL}/login"

    # ── 2. 定义元素定位器（类属性、元组格式）──
    USERNAME_INPUT = (By.CSS_SELECTOR, "input[placeholder*='手机号']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[type='password']")
    SUBMIT_BTN     = (By.CSS_SELECTOR, ".submit-btn")

    # ── 3. 定义业务方法 ──
    @allure.step("会员登录: {username}")
    def login(self, username, password, captcha="dev"):
        self.type(self.USERNAME_INPUT, username)
        self.type(self.PASSWORD_INPUT, password)
        self.click(self.CAPTCHA_BTN)
        self.type(self.CAPTCHA_INPUT, captcha)
        self.click(self.SUBMIT_BTN)

    # ── 4. 定义状态查询 ──
    def is_login_page(self):
        return self.is_displayed(self.TITLE)
```

**Page Object 的三条铁律：**

```
1. 定位器必须是类属性 → (By.CSS_SELECTOR, "...") 格式
2. 方法名体现业务语义 → login() 而非 click_submit_btn()
3. 不写 assert → 返回数据给用例判断
```

### 4.5 定位策略实战

```python
# ① 按 placeholder（Element Plus 组件最可靠的方式）
USERNAME_INPUT = (By.CSS_SELECTOR, "input[placeholder*='手机号']")

# ② 按文本内容（XPath 1.0）
SUBMIT_BTN = (By.XPATH, "//button[contains(.,'登录')]")

# ③ 多条件 OR 匹配
PAY_BTN = (By.XPATH, "//button[contains(.,'付款') or contains(.,'支付')]")

# ④ 按 CSS 类名 + 语义筛选
EMPTY = (By.CSS_SELECTOR, ".el-empty")

# ⑤ 后代选择器
ROW_CB = (By.CSS_SELECTOR, ".cart-row .el-checkbox")

# ⑥ 属性选择
PASSWORD_INPUT = (By.CSS_SELECTOR, "input[type='password']")
```

### 4.6 复合 Fixture — 预置登录状态

```python
# tests/cases/conftest.py

@pytest.fixture
def logged_in(driver, login_page, test_user):
    """依赖 driver + login_page + test_user 三个 fixture"""
    login_page.open()
    login_page.login(test_user["mobile"], test_user["password"])
    return test_user

# 使用：
def test_cart_page(cart_page, logged_in):
    cart_page.open()
    # ← 此时已经是登录状态
```

这样做的好处：
- 测试用例代码中**看不到登录操作**
- 一个 `logged_in` fixture 被多个用例复用
- 修改登录逻辑只需改一处

---

## 5. Allure 测试报告

### 5.1 注解体系

Allure 的四个核心注解形成了 BDD 风格的层级结构：

```
@allure.feature("大模块")         ← 一级：功能模块（如"会员登录"）
  @allure.story("子功能")          ← 二级：用户故事（如"正常登录"）
    @allure.severity(level)        ← 优先级（CRITICAL > NORMAL > MINOR）
    def test_xxx():
        ...
```

**本项目使用方式：**

```python
import allure

@allure.feature("会员登录")              # ← 标注在类上
class TestLogin:

    @allure.story("正常登录")            # ← 标注在方法上
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.p0
    def test_login_success(self, login_page, test_user):
        login_page.open()
        login_page.login(...)
```

**`@allure.step` — 在报告中显示操作步骤：**

```python
# BasePage 中的关键方法已标注
class BasePage:
    @allure.step("打开页面: {url}")       # {url} 会自动填充参数值
    def open(self, url): ...

    @allure.step("点击: {locator[1]}")    # {locator[1]} 显示选择器字符串
    def click(self, locator): ...

# 页面方法中使用
class LoginPage:
    @allure.step("会员登录: username={username}")
    def login(self, username, password): ...
```

### 5.2 自动环境信息

```python
# tests/conftest.py — pytest_configure 钩子

def pytest_configure(config):
    """在每个 Allure 报告中自动生成 environment.properties"""
    allure_dir = Path(config.getoption("--alluredir"))
    env_file = allure_dir / "environment.properties"
    with open(env_file, "w") as f:
        f.write(f"Browser={BROWSER}\n")
        f.write(f"BaseURL={BASE_URL}\n")
        f.write(f"Timestamp={datetime.now().isoformat()}\n")
```

在 Allure 报告中会显示：
```
Browser=chrome
BaseURL=http://localhost:3000
Timestamp=2026-06-24T10:30:00
```

### 5.3 失败自动截图

```python
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            # 截图
            driver.save_screenshot(str(filepath))
            allure.attach.file(filepath, name="失败截图",
                               attachment_type=allure.attachment_type.PNG)

            # 浏览器控制台日志
            logs = driver.get_log("browser")
            allure.attach(formatted_logs, name="浏览器控制台",
                          attachment_type=allure.attachment_type.TEXT)
```

**执行流程：**

```
用例失败 → hook 触发 → 截图 → 读浏览器日志 → 附加到 Allure
```

### 5.4 生成 Allure 报告

```bash
# 1. 运行测试（结果写入 allure-results）
pytest --alluredir=reports/allure-results

# 2. 在浏览器中查看报告
allure serve reports/allure-results

# 3. 生成静态 HTML（用于 CI/CD 发布）
allure generate reports/allure-results -o reports/allure-report
```

---

## 6. 测试配置管理

### 6.1 环境变量驱动的配置

```python
# tests/utils/config.py

import os
from pathlib import Path

# 每个配置项都支持环境变量覆盖
BASE_URL   = os.getenv("YUNSHOP_BASE_URL",   "http://localhost:3000")
BROWSER    = os.getenv("YUNSHOP_BROWSER",    "chrome").lower()
HEADLESS   = os.getenv("YUNSHOP_HEADLESS",   "false").lower() == "true"
TEST_USER  = {
    "mobile":   os.getenv("YUNSHOP_TEST_MOBILE",   "13800138000"),
    "password": os.getenv("YUNSHOP_TEST_PASSWORD", "Test@123"),
}
```

**设计要点：**

| 要点 | 说明 |
|------|------|
| 命名前缀 | 所有变量以 `YUNSHOP_` 开头，避免冲突 |
| 有默认值 | 开发环境无需设置任何环境变量即可运行 |
| 值类型转换 | `HEADLESS` 用 `== "true"` 转 bool，超时用 `int()` 转数字 |
| 复制保护 | `TEST_USER.copy()` 返回副本，防止用例修改全局配置 |

### 6.2 多环境运行

```bash
# 本地 Chrome 开发（默认，零配置）
pytest -m smoke

# CI/CD 无头 Chrome
YUNSHOP_HEADLESS=true pytest -v

# 切换到 Firefox
YUNSHOP_BROWSER=firefox pytest -v

# 测试预发布环境
YUNSHOP_BASE_URL=https://staging.yunshop.com pytest

# 全部自定义
YUNSHOP_BROWSER=edge \
YUNSHOP_HEADLESS=true \
YUNSHOP_BASE_URL=http://test-server:3000 \
pytest -v --alluredir=reports/allure-results
```

---

## 7. 数据驱动与测试数据管理

### 7.1 常量层 — 集中管理固定文案

```python
# tests/data/constants.py

# URL 片段
URL_HOME         = "/"
URL_LOGIN        = "/login"
URL_CART         = "/cart"

# 提示文案
MSG_LOGIN_SUCCESS  = "登录成功"
MSG_ADD_TO_CART_OK = "已加入购物车"
MSG_EMPTY_CART     = "购物车还没有任何商品，马上去购物"

# 页面标题
TITLE_LOGIN_PAGE    = "登录云集优选"
TITLE_ADMIN_LOGIN_PAGE = "云集优选 · 后台管理"

# Element Plus 类名
CLASS_EL_MESSAGE   = "el-message"
CLASS_EL_EMPTY     = "el-empty"
CLASS_EL_PAGINATION = "el-pagination"
```

**使用方式：**

```python
from data.constants import TITLE_LOGIN_PAGE, MSG_LOGIN_SUCCESS

def test_login_success(self, login_page):
    assert login_page.get_title_text() == TITLE_LOGIN_PAGE
```

**好处：UI 文案变了只需改一处，不用翻所有用例。**

### 7.2 动态数据生成器

```python
# tests/data/test_data.py

def new_mobile() -> str:
    """生成唯一手机号：1[3-9]xxxxxxxxx"""
    second = str(random.choice([3,4,5,6,7,8,9]))
    return f"1{second}{random_digits(9)}"

def new_email() -> str:
    """生成唯一邮箱：xxxx@[126|sina|qq|163].com"""
    domains = ["126.com", "sina.com", "qq.com", "163.com"]
    return f"{random_string(4)}{random_digits(4)}@{random.choice(domains)}"

def new_goods_data() -> dict:
    """生成商品数据"""
    ts = timestamp()[-8:]
    return {
        "goods_name": f"测试商品_{ts}",
        "goods_sn": f"TESTSN{ts}",
        "shop_price": str(round(random.uniform(10, 5000), 2)),
        "store_count": str(random.randint(1, 999)),
    }
```

**数据生成器设计原则：**

```
1. 唯一性 → 用毫秒时间戳 + 随机数
2. 合规性 → 符合业务规则（手机号11位、邮箱域名白名单）
3. 可读性 → 带 "测试_" 前缀，方便人工识别
4. 不可变性 → 函数式设计，每次调用返回新值
```

---

## 8. WebDriver 工厂模式

### 8.1 多浏览器支持

```python
# tests/utils/driver_factory.py

def create_driver():
    """根据配置选择浏览器"""
    factories = {
        "chrome":  _create_chrome,
        "firefox": _create_firefox,
        "edge":    _create_edge,
    }
    driver = factories[BROWSER]()
    _configure_timeouts(driver)
    return driver
```

### 8.2 Chrome 反检测配置

```python
def _create_chrome():
    options = ChromeOptions()
    # 无头模式
    if HEADLESS:
        options.add_argument("--headless=new")

    # 容器环境必需
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # 隐藏自动化标记（防止网站拒绝自动化浏览器）
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
```

### 8.3 自动驱动管理

```python
try:
    from webdriver_manager.chrome import ChromeDriverManager
    service = ChromeService(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)
except ImportError:
    # 降级：使用系统 PATH 中的驱动
    return webdriver.Chrome(options=options)
```

**`webdriver-manager` 自动做什么：**

```
1. 检测你本机的 Chrome 版本号
2. 自动下载匹配的 ChromeDriver 版本
3. 缓存到本地，下次直接使用
4. 如果未安装 → 降级使用系统 PATH 中的驱动
```

### 8.4 Driver Fixture 生命周期

```python
@pytest.fixture(scope="function")
def driver() -> Generator[webdriver.Remote, None, None]:
    # === Setup ===
    drv = create_driver()           # ① 创建浏览器实例
    yield drv                       # ② 用例执行

    # === Teardown ===
    drv.quit()                      # ③ 关闭浏览器
```

```
用例1: create → test_login →  quit
用例2: create → test_register → quit
用例3: create → test_home → quit
```

---

## 9. 日志系统

### 9.1 双通道日志

```python
# tests/utils/logger.py

def get_logger(name="yunshop_test"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # 控制台 — INFO 级别（不刷屏）
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)

    # 文件 — DEBUG 级别（完整记录）
    file_handler = logging.FileHandler("reports/logs/test_run.log")
    file_handler.setLevel(logging.DEBUG)

    logger.addHandler(console)
    logger.addHandler(file_handler)
    return logger
```

### 9.2 日志使用示例

```python
logger.info(">>> 创建 WebDriver 实例")          # 关键节点
logger.info("WebDriver 初始化完成 — 浏览器: %s", BROWSER)  # 参数化
logger.warning("webdriver-manager 未安装")       # 警告
logger.error(">>> WebDriver 异常: %s", e)        # 错误
logger.debug("详细信息...")                        # 调试信息（仅文件）
```

---

## 10. Element Plus 组件测试技巧

### 10.1 下拉选择（el-select）

Element Plus 的 `<el-select>` 渲染成 div，不是原生 `<select>`，不能用 `Select()` 类。

```python
def el_select_option(self, select_placeholder, option_text):
    """Element Plus 下拉选择专用方法"""
    # ① 点击触发器
    trigger = (By.XPATH, f"//input[@placeholder='{select_placeholder}']")
    self.click(trigger)

    # ② 等待并点击下拉选项
    option = (By.XPATH,
        f"//div[contains(@class,'el-select-dropdown')]"
        f"//li[contains(@class,'el-select-dropdown__item')]"
        f"/span[text()='{option_text}']")
    self.click(option)
```

### 10.2 消息提示（el-message）

```python
def el_message_should_contain(self, text):
    """验证 el-message 提示内容"""
    locator = (By.CSS_SELECTOR, ".el-message .el-message__content")
    try:
        actual = self.get_text(locator)
        return text in actual
    except TimeoutException:
        return False
```

### 10.3 对话框（el-dialog / el-message-box）

```python
# 点击确认
btn = (By.CSS_SELECTOR, ".el-message-box__btns .el-button--primary")
self.click(btn)

# 点击取消
btn = (By.CSS_SELECTOR, ".el-message-box__btns .el-button:not(.el-button--primary)")
self.click(btn)
```

### 10.4 输入框（el-input）

```python
# 按 placeholder 定位（最可靠）
input = (By.CSS_SELECTOR, "input[placeholder*='手机号']")

# 按 type 定位
password = (By.CSS_SELECTOR, "input[type='password']")

# 获取当前值
value = self.get_value(locator)  # 读 value 属性
```

### 10.5 计数器（el-input-number）

```python
# 定位内部 input
NUM_INPUT = (By.CSS_SELECTOR, ".el-input-number .el-input__inner")

# 点击 + 按钮
INCREASE = (By.CSS_SELECTOR, ".el-input-number__increase")

# 点击 - 按钮
DECREASE = (By.CSS_SELECTOR, ".el-input-number__decrease")
```

---

## 11. 实战：编写一条完整用例

### 11.1 Step by Step

以「正常登录成功」为例，串联所有知识点：

```python
"""
会员登录 — 测试用例
"""
import allure
import pytest

from data.constants import TITLE_LOGIN_PAGE, URL_HOME


@allure.feature("会员登录")               # ← Allure 一级分类
class TestLogin:

    @allure.story("正常登录")              # ← Allure 二级分类
    @allure.severity(allure.severity_level.CRITICAL)  # ← 优先级
    @pytest.mark.smoke                    # ← pytest 标记：冒烟
    @pytest.mark.p0                       # ← pytest 标记：P0
    def test_login_success(self, login_page, test_user):  # ← fixture 注入
        """使用正确凭证登录，验证跳转到首页。"""

        # ① 打开页面
        login_page.open()

        # ② 前置断言：确认在登录页
        assert login_page.is_login_page(), "应位于登录页"
        assert login_page.get_title_text() == TITLE_LOGIN_PAGE

        # ③ 执行业务操作
        login_page.login(
            username=test_user["mobile"],     # ← 从 fixture 获取
            password=test_user["password"],
        )

        # ④ 断言结果：等待 URL 跳转
        assert login_page.wait_for_url_contains(URL_HOME, timeout=5)
```

### 11.2 数据流全链路追踪

```
① pytest 发现用例 → 解析参数 → 遇到 login_page fixture
② 进入 cases/conftest.py → login_page fixture 需要 driver
③ 进入 tests/conftest.py → driver fixture → create_driver()
④ driver_factory.py → 根据 config.BROWSER 创建 Chrome/Firefox/Edge
⑤ 返回 driver → 注入 LoginPage(driver) → 注入 test_user dict
⑥ 执行 test_login_success()
⑦ 每一步 click/type 都通过 BasePage 的 @allure.step 记录
⑧ 断言通过 → driver fixture teardown → driver.quit()
⑨ 断言失败 → pytest_runtest_makereport 钩子 → 截图 + 控制台日志
```

### 11.3 运行这条用例

```bash
# 只跑这条
pytest tests/cases/front/test_login.py::TestLogin::test_login_success -v

# 跑整个登录模块
pytest tests/cases/front/test_login.py -v

# 带 Allure 报告
pytest tests/cases/front/test_login.py --alluredir=reports/allure-results
allure serve reports/allure-results
```

---

## 附录

### A. 完整文件索引

| 文件 | 行数 | 知识点 |
|------|------|--------|
| `tests/conftest.py` | 169 | Hook、Fixture Scope、Generator、环境变量注入 |
| `tests/pytest.ini` | 15 | Markers 注册、addopts 配置 |
| `tests/utils/config.py` | 45 | os.getenv 模式、Path 对象、条件类型转换 |
| `tests/utils/driver_factory.py` | 101 | 工厂模式、Options 配置、多浏览器、降级策略 |
| `tests/utils/logger.py` | 35 | 双通道日志、handler 防重复 |
| `tests/pages/base_page.py` | 497 | 显式等待大全、ActionChains、JS 执行、Element Plus 适配 |
| `tests/pages/front/login_page.py` | 65 | Page Object 模板、@allure.step |
| `tests/cases/conftest.py` | 167 | fixture 工厂、复合 fixture |
| `tests/cases/front/test_login.py` | 85 | Allure 注解、parametrize、断言模式 |
| `tests/data/constants.py` | 40 | 常量管理 |
| `tests/data/test_data.py` | 70 | 随机数据生成、唯一性策略 |

### B. 常用命令速查表

```bash
# ─── 运行筛选 ───
pytest -m smoke                            # 冒烟测试
pytest -m "front and p0"                   # 前台 P0
pytest -m "not login_required"             # 跳过需登录的
pytest -k "test_login"                     # 按函数名匹配
pytest -k "test_login or test_register"    # 多关键词

# ─── 报告 ───
pytest --alluredir=reports/allure-results  # 生成 Allure 数据
allure serve reports/allure-results        # 浏览器查看
allure generate -o reports/allure-report   # 静态 HTML

# ─── 调试 ───
pytest -x                                  # 失败即停
pytest --lf                                # 只重跑上次失败的
pytest --tb=long                           # 长回溯
pytest -s                                  # 显示 print 输出

# ─── 环境变量 ───
YUNSHOP_HEADLESS=true pytest               # 无头模式
YUNSHOP_BROWSER=firefox pytest             # Firefox
YUNSHOP_BASE_URL=http://test:3000 pytest   # 自定义地址
```

### C. 框架设计原则总结

```
1. 单一职责    → BasePage 只做操作，Page Object 只做封装，用例只做断言
2. 开闭原则    → 加新页面只需新建 Page Object，不改 BasePage
3. 依赖倒置    → 用例依赖 fixture 抽象，不直接 new 对象
4. 显式优于隐式 → 用 WebDriverWait 不用 time.sleep
5. 配置外部化  → 环境变量而非硬编码
6. 失败可追溯  → 自动截图 + 日志 + Allure 报告
```
