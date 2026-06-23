# 云集优选 YunShop

<p align="center">
  <b>B2C 电商平台 — SpringBoot 3 + Vue 3 全栈重构版</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Java-17-brightgreen" alt="Java 17">
  <img src="https://img.shields.io/badge/SpringBoot-3.2.10-brightgreen" alt="SpringBoot 3.2.10">
  <img src="https://img.shields.io/badge/Vue-3.4-brightgreen" alt="Vue 3.4">
  <img src="https://img.shields.io/badge/Vite-5-blue" alt="Vite 5">
  <img src="https://img.shields.io/badge/Element_Plus-2.8-blue" alt="Element Plus 2.8">
  <img src="https://img.shields.io/badge/MySQL-8.0-orange" alt="MySQL 8.0">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
</p>

## 📖 项目简介

云集优选是一个面向**自动化测试练习**的 B2C 电商平台，采用前后端分离架构。项目模拟了真实电商系统的主要业务流程：商品浏览 → 加入购物车 → 下单结算 → 支付发货。

**注意**：本项目定位为教学与测试练习用途，部分高级功能尚未实现（详见 [需求文档](docs/YUNshop_需求文档.md) 中的实现状态）。

## ✨ 核心功能

| 模块 | 功能 |
|------|------|
| 🏠 首页 | 三级分类菜单 + 悬停下拉、Banner 轮播、商品楼层、热门推荐 |
| 🔍 商品 | 分类筛选、关键词搜索、价格/销量/新品排序、分页浏览 |
| 🛒 购物车 | 加入购物车、数量修改、全选/批量删除、20种上限 |
| 📦 订单 | 提交订单 → 支付 → 发货 → 确认收货，完整状态流转 |
| 👤 用户 | 注册/登录、头像上传、个人信息、订单管理、密码修改（含强度指示）、收货地址（最多20个） |
| 🖼️ 文件 | 头像图片上传（.png/.jpg，最大5MB），`/upload/**` 静态资源映射 |
| 🛡️ 后台 | 商品增删改查/上下架、仪表盘 |

## 🛠 技术栈

| 层级 | 技术 | 版本 |
|------|------|------|
| 后端框架 | Spring Boot | 3.2.10 |
| JDK | Java | 17 |
| ORM | MyBatis-Plus | 3.5.5 |
| 安全 | BCrypt (spring-security-crypto) | — |
| 校验 | spring-boot-starter-validation | — |
| 前端框架 | Vue 3 + Composition API | 3.4 |
| 构建工具 | Vite | 5 |
| UI 组件库 | Element Plus | 2.8 |
| HTTP 客户端 | Axios | 1.7 |
| 路由 | Vue Router | 4 |
| 数据库 | MySQL | 8.0 |
| 测试 | pytest + Selenium + Allure | 9.0 / 4.44 / 2.16 |

## 🚀 快速开始

### 环境要求

- **JDK 17+**
- **Maven 3.6+**
- **Node.js 18+**
- **MySQL 8.0+**（运行中）

### 1. 导入数据库

```bash
mysql -u root -p123456 < sql/schema.sql
mysql -u root -p123456 < sql/data.sql
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
| 前台首页 | http://localhost:3000/ | — |
| 后台管理 | http://localhost:3000/admin/login | admin / admin123 |

## 📁 项目结构

```
YunShop/
├── backend/                          # SpringBoot 后端（端口 8080）
│   ├── pom.xml                       # Maven 依赖
│   └── src/main/java/com/yunshop/
│       ├── YunShopApplication.java   # 启动类
│       ├── common/                   # Result<T>、PageResult、Constants
│       ├── config/                   # CORS、MyBatis-Plus、DataInitializer
│       ├── controller/front/         # 前台 API（7个 Controller）
│       ├── controller/admin/         # 后台 API（2个 Controller）
│       ├── service/impl/             # 业务逻辑（12组）
│       ├── mapper/                   # MyBatis-Plus Mapper（18个）
│       ├── entity/                   # 实体类（18个）
│       └── dto/                      # 请求 DTO
├── frontend/                         # Vue 3 前端（端口 3000）
│   ├── vite.config.js                # 代理 /api → 8080
│   └── src/
│       ├── router/index.js           # 路由（前台13条 + 后台8条）
│       ├── api/                      # Axios 封装（按模块拆分）
│       ├── components/               # 共享组件（Header.vue）
│       └── views/front/ + admin/     # 页面组件
├── sql/                              # 建表 + 测试数据（18张表）
├── docs/                             # 需求文档 + API 文档
├── tests/                            # pytest + Selenium + PO + Allure（75条用例）
│   ├── conftest.py                    # 全局 fixtures（driver/截图/Allure）
│   ├── pytest.ini                     # 配置 + 6个自定义标记
│   ├── requirements.txt               # Python 依赖
│   ├── utils/                         # config / driver_factory / logger
│   ├── pages/                         # Page Object 层
│   │   ├── base_page.py               # 基类（50+ 通用方法）
│   │   ├── front/                     # 12个前台页面对象
│   │   └── admin/                     # 7个后台页面对象
│   ├── cases/                         # 测试用例层
│   │   ├── front/                     # 8个模块，45条前台用例
│   │   └── admin/                     # 2个模块，14条后台用例
│   └── data/                          # 常量 + 动态测试数据生成器
```

## 📡 API 文档

完整接口文档见 [docs/api.md](docs/api.md)，包含 47 个 REST API 的请求/响应示例。

**统一响应格式**：`{ "code": 200, "msg": "success", "data": ... }`

## 🗄️ 数据库

18 张表，无前缀，utf8mb4 字符集，全部使用逻辑删除（`is_deleted` 字段）。

核心表：`users`、`goods`、`goods_category`、`cart`、`order`、`order_goods`、`address`、`admin`、`ad`、`navigation`

## 🧪 测试

```bash
cd tests
pip install -r requirements.txt
pytest -m smoke --alluredir=reports/allure-results   # 冒烟测试
pytest -v                                             # 全部 75 条用例
allure serve reports/allure-results                   # 查看 Allure 报告
```

**框架特性**：Page Object 模式、BasePage 封装 50+ 通用操作、显式等待、失败自动截图、Allure 集成、环境变量驱动配置。

| 标记 | 用途 |
|------|------|
| `smoke` | 冒烟测试（核心流程） |
| `regression` | 回归测试 |
| `front` / `admin` | 前台 / 后台 |
| `login_required` | 需登录态 |
| `p0` / `p1` / `p2` | 用例优先级 |

## 📝 开发说明

- **验证码跳过**：开发环境输入 `dev` 即可
- **管理员密码**：每次启动自动重置为 `admin123`（`DataInitializer`）
- **占位图片**：`/api/images/goods/{id}` 和 `/api/images/banner/{id}` 自动生成 SVG
- **CORS**：已配置允许跨域携带 Cookie

## 📄 License

MIT License — 详见 [LICENSE](LICENSE) 文件。



