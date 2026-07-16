#                       		    		   云集优选 YunShop

<p align="center">
  <b>B2C 电商平台 — SpringBoot 3 + Vue 3 全栈项目，专为自动化测试练习设计</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Java-17-brightgreen" alt="Java 17">
  <img src="https://img.shields.io/badge/SpringBoot-3.2.10-brightgreen" alt="SpringBoot 3.2.10">
  <img src="https://img.shields.io/badge/Vue-3.4-brightgreen" alt="Vue 3.4">
  <img src="https://img.shields.io/badge/Vite-5-blue" alt="Vite 5">
  <img src="https://img.shields.io/badge/Element_Plus-2.8-blue" alt="Element Plus 2.8">
  <img src="https://img.shields.io/badge/MySQL-8.0-orange" alt="MySQL 8.0">
  <img src="https://img.shields.io/badge/pytest-9.0-blue" alt="pytest 9.0">
  <img src="https://img.shields.io/badge/Selenium-4.44-green" alt="Selenium 4.44">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
</p>

---

## 📖 项目简介

云集优选是一个面向**自动化测试练习**的 B2C 电商平台，采用前后端分离架构。项目模拟了真实电商系统的主要业务流程：

```
商品浏览 → 加入购物车 → 下单结算 → 支付 → 发货 → 确认收货
```

项目定位为教学与测试练习用途，已实现登录注册、商品浏览搜索、购物车、订单流程、用户中心、后台管理等核心电商功能。部分高级功能尚未实现，详见 [需求文档](docs/YUNshop_需求文档.md)。

## ✨ 核心功能

| 模块 | 功能 |
|------|------|
| 🏠 首页 | 三级分类菜单 + 悬停下拉面板、Banner 轮播、商品楼层、热门推荐 |
| 🔍 商品 | 分类筛选、关键词搜索、价格/销量/新品排序、分页浏览 |
| 🛒 购物车 | 加入购物车、数量修改、全选/批量删除、去结算 |
| 📦 订单 | 提交订单 → 支付 → 发货 → 确认收货，完整状态流转 |
| 👤 用户 | 注册/登录、头像上传（jpg/png/webp）、个人信息、订单管理、密码修改、收货地址 |
| 🛡️ 后台 | 仪表盘、商品增删改查/上下架、分类/订单/会员管理（部分为占位页） |
| 🧪 测试 | **67 条自动化用例**，Page Object 模式 + Allure 可视化报告 |

## 🛠 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| 后端框架 | SpringBoot 3.2.10 + Java 17 | REST API，统一 `Result<T>` 响应格式 |
| ORM | MyBatis-Plus 3.5.5 | 18 张表，逻辑删除，下划线转驼峰 |
| 安全 | BCrypt (spring-security-crypto) | 密码加密存储 |
| 校验 | spring-boot-starter-validation | 请求参数校验 |
| 前端框架 | Vue 3.4 + Vite 5 | Composition API |
| UI 组件库 | Element Plus 2.8 | 统一 UI 风格 |
| HTTP | Axios 1.7 | `withCredentials: true` 携带 Cookie |
| 路由 | Vue Router 4 | 前台 13 条 + 后台 8 条 |
| 数据库 | MySQL 8.0 | utf8mb4，自动建库 |
| 测试 | pytest 9.0.3 / Selenium 4.44 / Allure 2.16 | 67 条用例，Page Object 模式 |

## 🚀 快速开始

### 环境要求

| 组件 | 版本 |
|------|------|
| JDK | 17+ |
| Maven | 3.6+ |
| Node.js | 18+ |
| MySQL | 8.0+（需运行中） |

### 1. 导入数据库

```bash
mysql -u root -p123456 < sql/schema.sql
mysql -u root -p123456 < sql/data.sql
mysql -u root -p123456 < sql/new_goods.sql   # 可选：导入 100 个扩展商品
```

验证：
```bash
mysql -u root -p123456 yunshop -e "SELECT COUNT(*) FROM goods; SELECT COUNT(*) FROM goods_category;"
```

### 2. 启动后端（端口 8080）

```bash
cd backend
mvn spring-boot:run
```

验证：
```bash
curl http://localhost:8080/api/home
```

### 3. 启动前端（端口 3000）

```bash
cd frontend
npm install        # 首次运行
npm run dev
```

### 4. 访问系统

| 入口 | 地址 | 账号 |
|------|------|------|
| 前台首页 | http://localhost:3000/ | 自行注册 |
| 后台管理 | http://localhost:3000/admin/login | admin / admin123 |

### 5. 运行自动化测试

```bash
cd tests
pip install pytest selenium allure-pytest webdriver-manager faker  # 首次安装依赖

python run_tests.py              # 全部测试
python run_tests.py smoke        # 冒烟测试（核心流程）
python run_tests.py front        # 仅前台测试
python run_tests.py admin        # 仅后台测试
pytest -m "front and p0"         # 组合标记
allure serve reports/allure-results  # 查看可视化报告
```

## 📁 项目结构

```
YunShop/
├── backend/                          # SpringBoot 后端（端口 8080）
│   ├── pom.xml
│   └── src/main/java/com/yunshop/
│       ├── YunShopApplication.java   # 启动类 (@MapperScan)
│       ├── common/                   # Result<T>、PageResult、Constants
│       ├── config/                   # CORS、MyBatis-Plus、DataInitializer
│       ├── controller/front/         # 前台 API（7 个 Controller）
│       ├── controller/admin/         # 后台 API（2 个 Controller）
│       ├── service/impl/             # 业务逻辑（12 组）
│       ├── mapper/                   # MyBatis-Plus Mapper（18 个）
│       ├── entity/                   # 实体类（18 张表）
│       └── dto/                      # 请求 DTO（5 个）
├── frontend/                         # Vue 3 前端（端口 3000）
│   ├── package.json
│   ├── vite.config.js                # 代理 /api → 8080，@ 别名
│   └── src/
│       ├── router/index.js           # 路由（前台 13 + 后台 8）
│       ├── api/                      # Axios 封装（6 个模块）
│       ├── components/               # 共享组件（Header.vue）
│       └── views/front/ + admin/     # 页面组件（前台 11 + 后台 7）
├── sql/                              # 建表 + 测试数据（18 张表）
│   ├── schema.sql                    # 建表语句
│   ├── data.sql                      # 基础测试数据
│   └── new_goods.sql                 # 扩展商品数据（100 个）
├── tests/                            # pytest + Selenium + Allure（67 条用例）
│   ├── conftest.py / pytest.ini / run_tests.py
│   ├── config/                       # 全局配置
│   ├── utils/                        # WebDriver 工厂、日志、JSON 读取
│   ├── pages/                        # Page Object 层（19 个页面对象）
│   │   ├── base_page.py              # 基类（~25 个通用方法）
│   │   ├── front/                    # 前台 12 个
│   │   └── admin/                    # 后台 7 个
│   ├── cases/                        # 测试用例层（10 个文件）
│   ├── data/                         # 动态数据生成 + JSON 参数化
│   └── reports/                      # Allure 结果 + 日志 + 截图
├── docs/                             # 项目文档
│   ├── YUNshop_需求文档.md           # 完整功能需求
│   ├── api.md                        # 47 个 REST API
│   ├── deployment.md                 # 全链路部署文档
│   ├── test-framework-tutorial.md    # 测试框架教程
│   ├── 框架代码逻辑详解.md           # 框架代码逻辑说明
│   └── 自动化测试框架文档.md         # 测试框架完整文档
```

## 📡 API 文档

完整接口文档见 [docs/api.md](docs/api.md)，包含 46 个 REST API 的请求/响应示例。

**统一响应格式**：`{ "code": 200, "msg": "success", "data": { ... } }`

| code | 含义 |
|------|------|
| 200 | 成功 |
| 401 | 未登录 |
| 500 | 业务错误（msg 含错误描述） |

## 🗄️ 数据库

18 张表，无前缀，utf8mb4 字符集，全部使用逻辑删除（`is_deleted` 字段）。

核心表：`users`、`goods`、`goods_category`、`cart`、`order`、`order_goods`、`address`、`admin`、`ad`、`navigation`、`brand`、`goods_image`、`goods_attr`、`admin_role`、`system_menu`、`system_config`、`article`、`promotion`

## 🧪 自动化测试

### 框架概览

采用 **Page Object 模式 + pytest fixture 依赖注入** 三层架构：

| 层级 | 说明 |
|------|------|
| 用例层（`cases/`） | 10 个测试文件，67 条用例，覆盖前台 + 后台核心流程 |
| 页面对象层（`pages/`） | 19 个 Page Object，封装元素定位和业务操作 |
| 基础设施层 | WebDriver 工厂、日志系统、动态数据生成、Allure 报告 |

### 运行命令

```bash
cd tests
pip install pytest selenium allure-pytest webdriver-manager faker

# 便捷脚本
python run_tests.py              # 全部测试
python run_tests.py smoke        # 冒烟测试（~8 条核心流程）
python run_tests.py front        # 仅前台
python run_tests.py admin        # 仅后台
python run_tests.py p0           # 仅 P0 级别

# pytest 直接运行
pytest -v                        # 全部，详细输出
pytest -m smoke                  # 按标记
pytest cases/front/test_login.py # 单文件
pytest -k "login_success"        # 按名称

# 查看报告
allure serve reports/allure-results
```

### 测试标记

| 标记 | 用途 |
|------|------|
| `smoke` / `regression` | 测试类型 |
| `front` / `admin` | 前台 / 后台 |
| `p0` / `p1` / `p2` | 优先级（核心 / 重要 / 边缘） |
| `login_required` | 需要登录态 |

### 框架特性

- **独立浏览器实例**：每个用例 function 级别隔离，互不影响
- **显式等待**：BasePage 所有查找操作均使用 `WebDriverWait`，适应异步渲染
- **失败自动截图**：失败时自动截图 + 浏览器控制台日志，附加到 Allure 报告
- **动态数据生成**：手机号、邮箱、商品数据等每次运行唯一，避免数据库冲突
- **复合登录 fixture**：`logged_in` / `admin_logged_in` 自动预置登录态

> 详细框架文档见 [tests/自动化测试框架文档.md](tests/自动化测试框架文档.md)

## 📝 开发说明

- **认证方式**：Session + Cookie，后端 CORS 已配置 `allowCredentials=true`
- **验证码跳过**：开发环境输入 `dev` 即可跳过验证码校验
- **管理员密码**：`DataInitializer` 每次启动自动重置为 `admin123`（BCrypt）
- **占位图片**：`/api/images/goods/{id}` 和 `/api/images/banner/{id}` 自动生成 SVG
- **订单状态**：PENDING → PAID → SHIPPED → COMPLETED，可 CANCEL
- **Header 组件**：仅首页使用了共享 `<Header />` 组件，其他页面使用简易 `top-bar`

## 📄 License

MIT License
