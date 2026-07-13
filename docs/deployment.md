# 云集优选 B2C 电商平台 — 全链路部署文档

> **最后更新**: 2026-07-13
>
> **适用环境**: Windows 10/11 Pro x64（其他系统需调整路径）

---

## 一、环境要求

| 组件 | 最低版本 | 本项目使用 | 验证命令 |
|------|----------|-----------|----------|
| JDK | 17 | 17.0.12 | `java -version` |
| Maven | 3.8 | 3.9.13 | `mvn -version` |
| MySQL | 8.0 | 8.0.45 | `mysql --version` |
| Node.js | 16 | 22.16.0 | `node -version` |
| npm | 8 | 10.9.2 | `npm -version` |

### 1.1 安装路径（示例）

| 工具 | 路径 |
|------|------|
| JDK | 任意路径（需配置 JAVA_HOME 环境变量） |
| Maven | 任意路径（需配置 MAVEN_HOME 并添加到 PATH） |
| MySQL | 默认安装路径或自定义路径 |

---

## 二、数据库初始化

### 2.1 确认 MySQL 服务运行

```powershell
# 检查服务状态
Get-Service MySQL80

# 如未启动
Start-Service MySQL80
```

### 2.2 创建数据库并导入数据

```bash
# 方式一：source 命令（推荐逐段执行）
mysql -u root -p123456

# 在 MySQL shell 中执行：
source sql/schema.sql;
source sql/data.sql;
source sql/new_goods.sql;   # 可选：导入 100 个扩展商品
exit;

# 方式二：管道导入
mysql -u root -p123456 < sql/schema.sql
mysql -u root -p123456 < sql/data.sql
mysql -u root -p123456 < sql/new_goods.sql   # 可选
```

> **注意**: 如果 `source` 命令遇到编码问题报 "Data too long"，请改用下面的直接插入方式。

### 2.3 直接插入命令（source 失败时使用）

```bash
# 插入管理员角色
mysql -u root -p123456 yunshop -e "
INSERT INTO admin_role (role_id, role_name, description, permissions, status) VALUES 
(1, '超级管理员', '所有权限', '{\"all\": true}', 1),
(2, '仓管员', '仓库管理', '{\"goods\":[\"view\",\"edit\"]}', 1),
(3, '客服', '订单处理', '{\"order\":[\"view\",\"edit\",\"ship\"]}', 1);
"

# 插入系统菜单
mysql -u root -p123456 yunshop -e "
INSERT INTO system_menu (id, name, url, parent_id, icon, sort_order, type) VALUES
(1, '系统设置', '/admin/system', 0, 'gear', 10, 'menu'),
(2, '商品管理', '/admin/goods', 0, 'box', 20, 'menu'),
(3, '订单管理', '/admin/order', 0, 'list-check', 30, 'menu'),
(4, '会员管理', '/admin/user', 0, 'people', 40, 'menu'),
(5, '广告管理', '/admin/ad', 0, 'image', 50, 'menu'),
(6, '文章管理', '/admin/article', 0, 'file-text', 60, 'menu'),
(7, '品牌管理', '/admin/brand', 0, 'tag', 70, 'menu'),
(8, '导航管理', '/admin/navigation', 0, 'link', 80, 'menu'),
(9, '促销管理', '/admin/promotion', 0, 'gift', 90, 'menu');
"

# 插入导航数据
mysql -u root -p123456 yunshop -e "
INSERT INTO navigation (id, name, url, sort_order, is_show, position) VALUES
(1, '首页', '/', 10, 1, 'top'),
(2, '手机数码', '/goods/list?catId=1', 20, 1, 'top'),
(3, '电脑办公', '/goods/list?catId=2', 30, 1, 'top'),
(4, '家用电器', '/goods/list?catId=3', 40, 1, 'top'),
(5, '服装鞋帽', '/goods/list?catId=4', 50, 1, 'top'),
(6, '食品生鲜', '/goods/list?catId=5', 60, 1, 'top'),
(7, '美妆个护', '/goods/list?catId=6', 70, 1, 'top'),
(8, '帮助中心', '/article/list', 80, 1, 'top');
"

# 插入商品分类（完整三级分类见 sql/data.sql）
# 插入品牌、商品、广告、配置等...
# 详细脚本参见 sql/data.sql
```

### 2.4 验证数据库

```sql
USE yunshop;
SELECT COUNT(*) AS user_count FROM users;
SELECT COUNT(*) AS goods_count FROM goods;
SELECT COUNT(*) AS category_count FROM goods_category;
SELECT * FROM admin;
```

预期结果:
| 表 | 预期行数 |
|------|---------|
| users | 0（注册后增加） |
| goods | 10 |
| goods_category | 28 |
| admin | 1 |
| brand | 6 |
| navigation | 8 |
| ad | 3 |

---

## 三、后端部署

### 3.1 配置文件

确认 `backend/src/main/resources/application.yml` 中的数据库密码正确：

```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/yunshop?useUnicode=true&characterEncoding=utf-8&serverTimezone=Asia/Shanghai&createDatabaseIfNotExist=true
    username: root
    password: 123456    # ← 确认此密码
```

### 3.2 编译

```bash
cd backend
mvn clean compile
```

### 3.3 启动

```bash
# 开发模式启动（终端前台运行）
cd backend
mvn spring-boot:run

# 或打包后运行
mvn clean package -DskipTests
java -jar target/yunshop-1.0.0.jar
```

### 3.4 验证后端

```bash
# 测试首页接口
curl http://localhost:8080/api/home

# 测试商品列表
curl http://localhost:8080/api/goods/list

# 测试后台登录
curl -X POST http://localhost:8080/api/admin/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

成功标志:
```
========================================
  云集优选 B2C 电商平台 启动成功！
  前台地址: http://localhost:8080/
  后台地址: http://localhost:8080/admin/login
========================================
```

---

## 四、前端部署

### 4.1 安装依赖

```bash
cd frontend
npm install
```

### 4.2 开发模式启动

```bash
cd frontend
npm run dev
```

启动后访问 `http://localhost:3000`

> Vite 会自动打开浏览器。如果 3000 端口被占用会尝试 3001。

### 4.3 生产构建

```bash
cd frontend
npm run build
# 产物在 dist/ 目录下
```

### 4.4 验证前端

浏览器访问：
- 前台首页: `http://localhost:3000/`
- 商品列表: `http://localhost:3000/goods/list`
- 后台登录: `http://localhost:3000/admin/login`

---

## 五、前后端联调

### 5.1 代理配置

前端 `vite.config.js` 中已配置代理：

```js
proxy: {
  '/api': { target: 'http://localhost:8080', changeOrigin: true },
  '/upload': { target: 'http://localhost:8080', changeOrigin: true }
}
```

### 5.2 CORS 配置

后端已配置 CORS 允许 `localhost` 任意端口的跨域请求（含 Cookie）。

### 5.3 完整测试流程

```
1. 启动 MySQL      (Get-Service MySQL80)
2. 启动后端        (cd backend && mvn spring-boot:run)
3. 启动前端        (cd frontend && npm run dev)
4. 浏览器访问       http://localhost:3000/
5. 注册账号         → 浏览商品 → 加入购物车 → 下单
6. 后台登录         http://localhost:3000/admin/login  (admin/admin123)
```

---

## 六、常见问题

### Q1: 编译报错 "不兼容的类型: Long 无法转换为 int"

**解决**: 使用 `.intValue()` 代替 `(int)` 强制转换。

### Q2: MySQL 密码不对

检查 `application.yml` 中 `spring.datasource.password`，确保与 MySQL root 密码一致。

### Q3: 数据库编码错误 "Data too long for column"

**解决**: 不用 `source` 命令，改用 `mysql -e` 直接执行 SQL。

### Q4: 端口 8080 被占用

```powershell
# 查找占用端口的进程
netstat -ano | findstr :8080
# 终止进程
taskkill /F /PID <进程ID>
```

### Q5: 前端 Vite 报 "Cannot resolve @/"

**解决**: 确保 `vite.config.js` 中配置了 `resolve.alias`。

### Q6: 登录失败 "验证码错误"

开发环境在验证码输入框中输入 `dev` 即可跳过验证码校验。

---

## 七、目录结构总览

```
├── backend/                         ← SpringBoot 后端
│   ├── pom.xml                      ← Maven 依赖
│   └── src/main/java/com/yunshop/
│       ├── YunShopApplication.java  ← 启动类
│       ├── common/                  ← 公共类（Result, PageResult, Constants）
│       ├── config/                  ← 配置（MyBatisPlus, CORS, Web, DataInit）
│       ├── entity/                  ← 实体类（18张表）
│       ├── mapper/                  ← MyBatis-Plus Mapper（18个）
│       ├── service/                 ← 业务接口 + 实现（12组）
│       ├── dto/                     ← 数据传输对象（5个）
│       └── controller/
│           ├── front/               ← 前台 API（7个）
│           └── admin/               ← 后台 API（2个）
├── frontend/                        ← Vue 3 前端
│   ├── package.json                 ← npm 依赖
│   ├── vite.config.js               ← Vite 配置（代理 + 别名）
│   ├── index.html                   ← 入口 HTML
│   └── src/
│       ├── main.js                  ← Vue 应用入口
│       ├── App.vue                  ← 根组件
│       ├── router/index.js          ← 路由配置（15条）
│       ├── api/                     ← API 请求封装（6个模块）
│       └── views/
│           ├── front/               ← 前台页面（14个）
│           └── admin/               ← 后台页面（7个）
├── sql/
│   ├── schema.sql                   ← 建表语句（18张表）
│   └── data.sql                     ← 测试数据
├── tests/                           ← pytest 自动化测试
└── docs/
    ├── YUNshop_需求文档.md           ← 需求文档
    ├── api.md                       ← API 接口文档（本文档）
    └── deployment.md                ← 全链路部署文档
```
