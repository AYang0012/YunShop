# 云集优选 B2C 电商平台 — API 接口文档

> **Base URL**: `http://localhost:8080/api`
>
> **认证方式**: Session + Cookie（前端自动携带，跨域已配置 `withCredentials: true`）
>
> **响应格式**: 统一 JSON 封装 `{ "code": 200, "msg": "success", "data": ... }`

---

## 一、前台接口

### 1.1 首页

#### `GET /api/home` — 获取首页全部数据

**请求参数**: 无

**响应示例**:
```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "navList": [
      { "id": 1, "name": "首页", "url": "/", "sortOrder": 10, "position": "top" }
    ],
    "categoryMenu": [
      {
        "category": { "id": 1, "name": "手机数码", "parentId": 0, "level": 1 },
        "children": [
          {
            "category": { "id": 11, "name": "手机", "parentId": 1, "level": 2 },
            "children": [
              { "id": 111, "name": "智能手机", "parentId": 11, "level": 3 }
            ]
          }
        ]
      }
    ],
    "bannerList": [
      { "adId": 1, "adName": "华为Mate60", "adImage": "/api/images/banner/1", "adLink": "/goods/detail/1", "type": "banner" }
    ],
    "floors": [
      {
        "category": { "id": 1, "name": "手机数码", "isHot": 1 },
        "subCategories": [{ "id": 11, "name": "手机" }],
        "goodsList": [{ "goodsId": 1, "goodsName": "华为Mate 60 Pro", "shopPrice": 6999.00 }]
      }
    ],
    "hotGoods": [
      { "goodsId": 1, "goodsName": "华为Mate 60 Pro", "shopPrice": 6999.00, "salesSum": 256 }
    ]
  }
}
```

#### `GET /api/categories/menu` — 获取分类菜单（含三级）

**请求参数**: 无

**响应**: 同上 `categoryMenu` 结构

---

### 1.2 用户

#### `GET /api/user/captcha` — 获取验证码

**请求参数**: 无

**响应**:
```json
{ "code": 200, "data": { "captcha": "A3X9" } }
```

#### `POST /api/user/login` — 会员登录

**请求体**:
```json
{ "username": "13800138000", "password": "Test@123", "captcha": "dev" }
```
> 开发环境设置 `captcha: "dev"` 可跳过验证码校验

**成功响应**:
```json
{ "code": 200, "msg": "登录成功", "data": { "userId": 1, "mobile": "13800138000", "nickname": "测试用户", "avatar": "/upload/avatars/avatar_1_a1b2c3d4.png" } }
```

**失败响应**:
```json
{ "code": 500, "msg": "用户名或密码错误" }
```

#### `POST /api/user/register` — 会员注册

**请求体**:
```json
{
  "account": "13800138000",
  "registerType": "mobile",
  "password": "Test@123",
  "confirmPassword": "Test@123",
  "referrerMobile": "",
  "agreeProtocol": true,
  "avatar": ""
}
```
> `avatar` 为可选字段，注册后可通过 `POST /api/upload/avatar` + `PUT /api/user/profile` 上传头像

**响应**: `{ "code": 200, "msg": "注册成功", "data": { ... } }`

**注册规则**:
| 规则 | 说明 |
|------|------|
| 手机号 | 11位，第一位为1，第二位非2 |
| 邮箱 | `xxxx@[126/sina/qq/163].com`，xxxx 长度4-16位 |
| 密码 | 6-16位，大小写+数字+符号（至少两种组合） |
| 协议 | 必须勾选同意 |

#### `POST /api/user/logout` — 安全退出

**请求参数**: 无

**响应**: `{ "code": 200, "msg": "已安全退出" }`

#### `GET /api/user/current` — 获取当前登录用户

**响应**:
```json
{ "code": 200, "data": { "userId": 1, "mobile": "13800138000", "nickname": "测试用户", "email": null, "avatar": "/upload/avatars/avatar_1_a1b2c3d4.png" } }
```
> 未登录返回 `{ "code": 401, "msg": "未登录" }`

#### `GET /api/user/check` — 登录状态检查

**响应**: `{ "code": 200, "data": true }` 或 `{ "code": 200, "data": false }`

#### `PUT /api/user/profile` — 更新个人信息

**请求体**:
```json
{ "nickname": "新昵称", "avatar": "/upload/avatars/avatar_1_a1b2c3d4.png" }
```
> `avatar` 字段为上传接口返回的相对路径

**响应**: `{ "code": 200, "msg": "更新成功" }`

#### `PUT /api/user/password` — 修改密码

**请求体**:
```json
{ "oldPassword": "Test@123", "newPassword": "NewPass@456" }
```

**响应**: `{ "code": 200, "msg": "密码修改成功" }`

---

### 1.3 商品

#### `GET /api/goods/list` — 商品列表（分页+筛选+排序+搜索）

**请求参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| catId | Long | 否 | 分类ID（含子分类） |
| keyword | String | 否 | 搜索关键词 |
| sort | String | 否 | 排序字段: `price` / `sales` / `time` |
| order | String | 否 | 排序方向: `asc` / `desc` |
| page | int | 否 | 页码（默认1） |
| pageSize | int | 否 | 每页条数: `12` / `24` / `48`（默认12） |

**请求示例**: `GET /api/goods/list?catId=1&sort=price&order=asc&page=1&pageSize=12`

**响应**:
```json
{
  "code": 200,
  "data": {
    "total": 100,
    "page": 1,
    "pageSize": 12,
    "totalPages": 9,
    "list": [
      {
        "goodsId": 1,
        "goodsSn": "SN20260601001",
        "goodsName": "华为Mate 60 Pro 智能手机 5G全网通",
        "catId": 111,
        "brandId": 1,
        "shopPrice": 6999.00,
        "marketPrice": 7999.00,
        "storeCount": 100,
        "salesSum": 256,
        "goodsThumb": "/api/images/goods/1",
        "isOnSale": 1,
        "isHot": 1,
        "isRecommend": 1
      }
    ]
  }
}
```

#### `GET /api/goods/detail/{goodsId}` — 商品详情

**响应**:
```json
{
  "code": 200,
  "data": {
    "goods": { "goodsId": 1, "goodsName": "...", "goodsContent": "<p>详情HTML</p>", "shopPrice": 6999.00, "marketPrice": 7999.00, "storeCount": 100, "salesSum": 256 },
    "images": [{ "imgId": 1, "imageUrl": "/api/images/goods/1", "isMain": 1 }],
    "attrs": [{ "goodsAttrId": 1, "attrName": "颜色", "attrValue": "雅川青", "attrPrice": 0.00, "storeCount": 50 }]
  }
}
```

#### `GET /api/goods/hot` — 热门推荐

**请求参数**: `limit`（默认8）

#### `GET /api/goods/search` — 关键词搜索

**请求参数**: `keyword`（必填）, `page`, `pageSize`

---

### 1.4 购物车

> **所有购物车接口需要登录态**

#### `GET /api/cart/list` — 购物车列表

**响应**:
```json
{
  "code": 200,
  "data": [
    {
      "cartId": 1,
      "goodsId": 1,
      "goodsName": "华为Mate 60 Pro",
      "goodsThumb": "/api/images/goods/1",
      "goodsPrice": 6999.00,
      "goodsNum": 2,
      "subtotal": 13998.00,
      "selected": 1,
      "storeCount": 100,
      "attrInfo": "颜色: 雅川青"
    }
  ]
}
```

#### `POST /api/cart/add` — 加入购物车

**请求体**:
```json
{ "goodsId": 1, "num": 1, "attrId": 0 }
```

**业务规则**:
- 单品最小: 1，最大: 200
- 购物车最多 20 种商品
- 已存在则累加数量

#### `PUT /api/cart/update/{cartId}` — 修改数量

**请求体**: `{ "num": 3 }`

#### `DELETE /api/cart/delete/{cartId}` — 删除单个

#### `POST /api/cart/delete-batch` — 批量删除

**请求体**: `{ "ids": [1, 2, 3] }`

#### `PUT /api/cart/toggle/{cartId}` — 切换选中状态

#### `PUT /api/cart/select-all` — 全选/取消全选

**请求体**: `{ "selected": true }`

#### `GET /api/cart/count` — 购物车商品种类数

---

### 1.5 订单

> **所有订单接口需要登录态**

#### `POST /api/order/submit` — 提交订单

**请求体**:
```json
{
  "addressId": 1,
  "cartIds": "1,2,3",
  "payName": "alipay",
  "shippingName": "express",
  "remark": "请尽快发货"
}
```
> `cartIds` 为要结算的购物车 ID，多个以逗号分隔

**响应**: `{ "code": 200, "msg": "下单成功", "data": { "orderId": 1, "orderSn": "20260621123456789001", ... } }`

#### `GET /api/order/list` — 订单列表

**请求参数**: `status`（可选，PENDING/PAID/SHIPPED/COMPLETED/CANCELLED）

#### `GET /api/order/detail/{orderId}` — 订单详情

**响应**: `{ "order": { ... }, "goodsList": [{ ... }] }`

#### `PUT /api/order/pay/{orderId}` — 模拟支付

#### `PUT /api/order/cancel/{orderId}` — 取消订单（仅待付款状态）

#### `PUT /api/order/receive/{orderId}` — 确认收货（仅已发货状态）

**订单状态流转**:
```
PENDING(待付款) → PAID(已付款) → SHIPPED(已发货) → COMPLETED(已完成)
    ↓                 
CANCELLED(已取消)    
```

---

### 1.6 收货地址

> **所有地址接口需要登录态**

#### `GET /api/address/list` — 地址列表

#### `GET /api/address/{addressId}` — 获取单个地址

#### `POST /api/address/add` — 新增地址

**请求体**:
```json
{ "consignee": "张三", "mobile": "13800138000", "province": "广东省", "city": "深圳市", "district": "南山区", "address": "科技园路100号" }
```
> 最多 20 个地址

#### `PUT /api/address/update` — 编辑地址

#### `DELETE /api/address/delete/{addressId}` — 删除地址

#### `PUT /api/address/default/{addressId}` — 设为默认地址

---

## 二、后台接口

### 2.1 管理员

#### `POST /api/admin/login` — 后台登录

**请求体**:
```json
{ "username": "admin", "password": "admin123" }
```

**响应**: `{ "code": 200, "msg": "登录成功", "data": { "adminId": 1, "username": "admin", "realName": "超级管理员" } }`

#### `POST /api/admin/logout` — 退出登录

#### `GET /api/admin/current` — 当前管理员信息

---

### 2.2 商品管理

> 需要管理员登录

#### `POST /api/admin/goods/add` — 添加商品

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| goodsName | String | 是 | 商品名称 |
| goodsSn | String | 是 | 商品编号 |
| catId | Long | 是 | 分类ID |
| brandId | Long | 否 | 品牌ID |
| shopPrice | BigDecimal | 是 | 售价 |
| marketPrice | BigDecimal | 否 | 原价 |
| storeCount | Integer | 是 | 库存 |
| isOnSale | Integer | 否 | 上架: 1 / 下架: 0 |
| isRecommend | Integer | 否 | 推荐: 1 / 否: 0 |
| goodsContent | String | 否 | 商品详情 HTML |

#### `PUT /api/admin/goods/update` — 更新商品

#### `DELETE /api/admin/goods/delete/{goodsId}` — 删除商品（软删除）

#### `PUT /api/admin/goods/toggle/{goodsId}` — 上下架切换

---

## 三、图片接口

#### `GET /api/images/goods/{goodsId}` — 商品占位图（PNG，400×400）

> 根据 goodsId 自动生成不同配色的 SVG 占位图

#### `GET /api/images/banner/{adId}` — Banner 占位图（PNG，800×400）

---

## 三、文件上传

> 需要登录态

#### `POST /api/upload/avatar` — 上传头像

**请求格式**: `multipart/form-data`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| file | File | 是 | 图片文件，支持 .png/.jpg/.jpeg/.webp，最大 5MB |

**成功响应**:
```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "url": "/upload/avatars/avatar_1_a1b2c3d4.png",
    "filename": "avatar_1_a1b2c3d4.png"
  }
}
```

> 上传成功后，将返回的 `url` 传入 `PUT /api/user/profile` 的 `avatar` 字段即可完成头像设置

---

## 四、错误码

| code | 说明 |
|------|------|
| 200 | 成功 |
| 401 | 未登录 |
| 500 | 业务错误（msg 中有具体描述） |
