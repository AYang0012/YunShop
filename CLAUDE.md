# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目定义

云集优选（YunShop）B2C 电商平台 — SpringBoot + Vue 3 重构版，唯一用途是**自动化测试练习**。

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端框架 | SpringBoot 3.2.10 + Java 17 |
| ORM | MyBatis-Plus 3.5.5 |
| 密码加密 | BCrypt (spring-security-crypto) |
| 参数校验 | spring-boot-starter-validation |
| 前端框架 | Vue 3.4 + Vite 5 + Vue Router 4 |
| UI 组件库 | Element Plus 2.8 |
| HTTP 客户端 | Axios 1.7 |
| 数据库 | MySQL 8.0.45 |
| 测试框架 | pytest 9.0.3 + Selenium 4.44.0（待编写） |

## 目录结构

```
G:\TestProject\
├── CLAUDE.md                        ← 项目定义文件（本文件）
├── backend/                         ← SpringBoot 后端（端口 8080）
│   ├── pom.xml                      ← Maven 依赖
│   ├── src/main/java/com/yunshop/
│   │   ├── YunShopApplication.java  ← 启动类（@MapperScan）
│   │   ├── common/                  ← Result<T>、PageResult、Constants
│   │   ├── config/                  ← CorsConfig、MyBatisPlusConfig、WebConfig、DataInitializer
│   │   ├── controller/front/       ← 前台 REST API（7个Controller）
│   │   ├── controller/admin/       ← 后台 REST API（2个Controller）
│   │   ├── service/ + service/impl/ ← 业务逻辑（12组 service + impl）
│   │   ├── mapper/                  ← MyBatis-Plus Mapper 接口（18个）
│   │   ├── entity/                  ← 实体类，映射数据库表（18个）
│   │   └── dto/                     ← 请求 DTO（LoginDto、RegisterDto、GoodsQueryDto、CartItemDto、OrderSubmitDto）
│   └── src/main/resources/
│       ├── application.yml          ← 数据库连接、MyBatis-Plus、上传路径配置
│       └── static/upload/           ← 文件上传目录
├── frontend/                        ← Vue 3 前端（端口 3000，Vite 代理 /api → 8080）
│   ├── package.json                 ← npm 脚本: dev / build / preview
│   ├── vite.config.js               ← 代理 + @ 别名配置
│   ├── index.html                   ← SPA 入口
│   └── src/
│       ├── main.js                  ← Vue 应用创建（Element Plus + Router + Icons）
│       ├── App.vue                  ← 根组件（仅 `<router-view />`）
│       ├── router/index.js          ← 路由（前台13条 + 后台8条）
│       ├── api/                     ← axios 请求封装（index/user/goods/cart/order/address.js）
│       ├── components/              ← 共享组件（当前仅 Header.vue）
│       └── views/front/ + admin/    ← 页面组件（前台11个 + 后台7个）
├── sql/
│   ├── schema.sql                   ← 建表语句（18张表，utf8mb4）
│   └── data.sql                     ← 测试数据（分类/品牌/商品/导航/广告等）
├── tests/                           ← pytest 自动化测试（目录已创建，测试用例待编写）
│   ├── conftest.py / pytest.ini
│   ├── pages/ / cases/front/ / cases/admin/ / data/ / reports/
├── scripts/                         ← 工具脚本
│   ├── download_images.py           ← 商品图片下载
│   └── generate_svg_images.py       ← SVG 占位图生成
└── docs/
    ├── YUNshop_需求文档.md           ← 完整功能需求
    ├── api.md                       ← REST API 接口文档（含请求/响应示例）
    └── deployment.md                ← 全链路部署文档（环境/数据库/前后端启动）
```

## 核心数据库表（18张，无前缀）

```sql
-- 数据库名: yunshop，字符集: utf8mb4
users            -- 会员（user_id, mobile, email, password[BCrypt], nickname, level, points）
goods_category   -- 商品分类，三级（id, name, parent_id, level, is_hot）
goods            -- 商品（goods_id, goods_name, cat_id, brand_id, shop_price, store_count, is_on_sale, is_recommend）
goods_image      -- 商品图片
goods_attr       -- 商品属性/规格（颜色、版本等，含库存和价格）
brand            -- 品牌
cart             -- 购物车（user_id, goods_id, goods_num, selected, attr_id）
`order`          -- 订单（order_sn, user_id, order_status, pay_name, shipping_name, total_amount）
order_goods      -- 订单商品明细
address          -- 收货地址（user_id, consignee, mobile, province/city/district, is_default）
admin            -- 管理员（admin_id, username, password[BCrypt], role_id）
admin_role       -- 管理员角色（权限 JSON: {"all": true}）
system_menu      -- 后台菜单
system_config    -- 系统配置（key-value）
article          -- 文章/帮助中心
ad               -- 广告（Banner）
navigation       -- 导航栏（position: top）
promotion        -- 促销活动
```

> 所有表使用逻辑删除（`is_deleted` 字段），MyBatis-Plus `@TableLogic` 自动处理。

## 常用命令

### 数据库

```bash
# 导入建表和数据（在 MySQL shell 中或管道）
mysql -u root -p123456 < G:/TestProject/sql/schema.sql
mysql -u root -p123456 < G:/TestProject/sql/data.sql

# 验证
mysql -u root -p123456 yunshop -e "SELECT COUNT(*) FROM goods; SELECT COUNT(*) FROM goods_category;"
```

### 后端

```bash
cd G:\TestProject\backend

# 编译
mvn clean compile

# 开发模式启动（前台运行，Ctrl+C 停止）
mvn spring-boot:run

# 打包并运行
mvn clean package -DskipTests
java -jar target/yunshop-1.0.0.jar

# 快速验证
curl http://localhost:8080/api/home
curl -X POST http://localhost:8080/api/admin/login -H "Content-Type: application/json" -d '{"username":"admin","password":"admin123"}'
```

### 前端

```bash
cd G:\TestProject\frontend

# 首次运行需安装依赖
npm install

# 开发模式启动（热更新，端口 3000）
npm run dev

# 生产构建
npm run build
```

### 完整启动流程

```
1. MySQL 服务运行  →  Get-Service MySQL80
2. 启动后端        →  cd backend && mvn spring-boot:run
3. 启动前端        →  cd frontend && npm run dev
4. 访问前台        →  http://localhost:3000/
5. 访问后台        →  http://localhost:3000/admin/login
```

## 重要实现细节

### 统一响应格式

所有 API 返回 `Result<T>` JSON：`{ "code": 200, "msg": "success", "data": ... }`。code=200 成功，401 未登录，500 业务错误（msg 中有描述）。

### 共享 Header 组件

`frontend/src/components/Header.vue` — 自包含的导航头部组件（无 props），自行加载所有数据：
- 调用 `getHomeData()` 获取导航项列表 (`navList`) 和分类菜单 (`categoryMenu`)
- 调用 `checkLogin()` + `getCurrentUser()` 获取登录态
- 调用 `getCartCount()` 获取购物车数量

### 悬停下拉菜单（Mega Dropdown）

顶部导航栏和首页左侧分类菜单均支持悬停展开：

- **Header.vue**：悬停导航项（如「手机数码」）→ 解析 URL 中的 `catId` → 匹配 `categoryMenu` 三级分类树 → 展开全宽下拉面板（毛玻璃效果，列+标签布局）
- **Home.vue**：悬停左侧分类项 → 弹出侧边面板（同样三级结构）
- 交互采用 150ms 防抖延迟消失，防止鼠标快速划过时闪烁
- **重要**：`/api/home` 的 `categoryMenu` 必须返回完整 3 层结构（`{category, children: [{category, children: [...]}]}`），否则下拉内容为空

### Header 迁移状态

目前**仅 Home.vue 使用了共享 `<Header />` 组件**，其他前台页面（GoodsList、Cart、GoodsDetail、OrderConfirm、OrderDetail、UserCenter 等）仍使用内联 `<header class="top-bar">`，功能较弱（仅 Logo + 页面标题，无导航菜单/用户区/购物车）。后续应考虑统一迁移到共享组件。

### 首页轮播图

Home.vue 使用**自定义 CSS 轮播**，非 Element Plus 组件：
- `transform: translateX` 滑动 + `transition: 0.5s cubic-bezier`
- `setInterval` 3 秒自动播放，鼠标悬停暂停
- 支持左右箭头、指示器圆点点击切换
- 兼容 0/1/2+ 张 Banner 场景

### 认证方式

Session + Cookie，后端 CORS 已配置允许跨域携带 Cookie（`allowCredentials=true`）。前端 axios 配置 `withCredentials: true`。

### 开发环境便利功能

- **验证码跳过**：登录时验证码输入 `dev` 即可跳过校验
- **管理员密码自动重置**：`DataInitializer` 在每次启动时将 admin 密码重置为 `admin123`（BCrypt 加密）
- **图片接口**：`/api/images/goods/{id}` 和 `/api/images/banner/{id}` 自动生成 SVG 占位图，无需真实图片文件

### 订单状态流转

```
PENDING(待付款) → PAID(已付款) → SHIPPED(已发货) → COMPLETED(已完成)
    ↓
CANCELLED(已取消)
```

### 前台路由（Vue Router）

| 路径 | 页面 |
|------|------|
| `/` | 首页（分类菜单 + Banner + 楼层 + 热销） |
| `/login` / `/register` | 登录 / 注册 |
| `/goods/list` | 商品列表（筛选/排序/分页） |
| `/goods/detail/:id` | 商品详情 |
| `/cart` | 购物车 |
| `/order/confirm` / `/order/detail/:id` | 下单确认 / 订单详情 |
| `/user` | 个人中心 |
| `/user/orders` / `/user/address` / `/user/profile` / `/user/password` | 订单/地址/资料/密码 |

### 后台路由（需登录 admin/admin123）

| 路径 | 页面 |
|------|------|
| `/admin/login` | 后台登录 |
| `/admin` | 仪表盘 |
| `/admin/goods` / `/admin/goods/edit/:id?` | 商品列表 / 添加编辑 |
| `/admin/category` | 分类管理 |
| `/admin/order` / `/admin/user` | 订单 / 会员管理 |

### 环境配置摘要

```yaml
# backend/src/main/resources/application.yml
server.port: 8080
spring.datasource.url: jdbc:mysql://localhost:3306/yunshop?...&createDatabaseIfNotExist=true
spring.datasource.username: root
spring.datasource.password: 123456

# MyBatis-Plus
mybatis-plus.configuration.map-underscore-to-camel-case: true     # users.user_id → userId
mybatis-plus.global-config.db-config.logic-delete-field: isDeleted # @TableLogic

# 文件上传路径
upload.path: ./src/main/resources/static/upload/
```

## 代码风格约定

- Java 包路径：`com.yunshop`
- 不使用 Lombok 注解生成 getter/setter（尽管依赖中已包含），手写 getter/setter
- Controller 按前台/后台分包：`controller.front.*` / `controller.admin.*`
- Service 接口 + Impl 实现类分离
- Entity 使用 MyBatis-Plus 注解：`@TableName`、`@TableId`、`@TableLogic`
- 前端 API 模块按功能拆分（`api/index.js` 封装 axios 实例，`api/user.js`、`api/goods.js` 等调用）
- 前端页面按前台/后台分包：`views/front/` / `views/admin/`
