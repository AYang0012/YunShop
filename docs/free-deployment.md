# 免费部署指南 — 云集优选 YunShop

> 前后端合并部署到 Render（免费层），一个 URL 访问完整应用

## 架构

```
https://yunshop.onrender.com
├── /api/*          → SpringBoot REST API
├── /upload/*       → 上传文件（头像、商品图片）
├── /goods/*        → Vue SPA（Vue Router 处理）
├── /admin/*        → Vue SPA（后台管理）
└── /login, /cart... → Vue SPA（前台页面）
```

## 第一步：注册 TiDB Cloud（免费 MySQL）

1. 访问 https://tidbcloud.com/signup 注册账号
2. 创建免费集群（Serverless，5GB 存储）
3. 在「Connect」页面获取连接信息：
   - Host: `xxx.tidbcloud.com`
   - Port: `4000`
   - User: `xxx.root`
   - Password: 创建时设置的密码
   - Database: `test`（默认数据库，可改名为 yunshop）

4. 导入数据库：

```bash
# 修改连接信息后执行
mysql -h <host> -P 4000 -u <user> -p<password> < sql/schema.sql
mysql -h <host> -P 4000 -u <user> -p<password> < sql/data.sql
```

> 注意：TiDB 的连接 URL 格式为：
> `jdbc:mysql://<host>:4000/yunshop?useSSL=true&serverTimezone=Asia/Shanghai`

## 第二步：部署到 Render

1. 访问 https://render.com 注册账号（可用 GitHub 登录）

2. 点击 **New +** → **Web Service**

3. 连接 GitHub 仓库：`AYang0012/YunShop`

4. 配置：
   - **Name**: `yunshop`
   - **Runtime**: `Java 17`
   - **Build Command**:
     ```
     cd frontend && npm install && npm run build && mkdir -p ../backend/src/main/resources/static/frontend && cp -r dist/* ../backend/src/main/resources/static/frontend/ && cd ../backend && mvn clean package -DskipTests
     ```
   - **Start Command**:
     ```
     java -jar backend/target/yunshop-1.0.0.jar
     ```

5. 在 **Environment Variables** 中添加：

   | Key | Value |
   |-----|-------|
   | `DB_URL` | `jdbc:mysql://<tidb-host>:4000/yunshop?useSSL=true&serverTimezone=Asia/Shanghai` |
   | `DB_USERNAME` | `<tidb-user>` |
   | `DB_PASSWORD` | `<tidb-password>` |

6. 点击 **Create Web Service**，等待部署完成（约 5-10 分钟）

## 第三步：访问

部署完成后，Render 会分配一个 URL：
```
https://yunshop.onrender.com
```

- 前台首页：`https://yunshop.onrender.com/`
- 后台管理：`https://yunshop.onrender.com/admin/login`（admin / admin123）

## 注意事项

### 免费层限制
- **15 分钟无请求自动休眠**
- 首次访问需等待 **30 秒左右唤醒**
- 唤醒后正常响应

### 数据库
- TiDB Cloud 免费层：5GB 存储，足够练习使用
- 需要将 `DB_URL` 中的 `createDatabaseIfNotExist=true` 去掉（TiDB 不支持此参数）

### 图片
- 商品图片存储在后端本地，Render 免费层**不支持持久化磁盘**
- 重启后上传的图片会丢失，但 `data.sql` 中的商品图片 URL 仍可访问
- 如需持久化，可将图片上传到外部图床（如 Cloudinary 免费层）

### 自定义域名（可选）
- Render 免费层支持绑定自定义域名
- 需要自己购买域名并配置 DNS
