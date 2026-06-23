-- ===============================================
-- 云集优选 B2C 电商平台 - 建表脚本
-- 数据库: yunshop
-- 字符集: utf8mb4
-- ===============================================

CREATE DATABASE IF NOT EXISTS yunshop
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

USE yunshop;

-- ===============================================
-- 1. 会员表
-- ===============================================
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
    `user_id`       BIGINT          NOT NULL AUTO_INCREMENT  COMMENT '用户ID',
    `mobile`        VARCHAR(20)     DEFAULT NULL             COMMENT '手机号',
    `email`         VARCHAR(100)    DEFAULT NULL             COMMENT '邮箱',
    `password`      VARCHAR(255)    NOT NULL                 COMMENT '密码(BCrypt加密)',
    `nickname`      VARCHAR(50)     DEFAULT NULL             COMMENT '昵称',
    `avatar`        VARCHAR(255)    DEFAULT NULL             COMMENT '头像URL',
    `level`         TINYINT         DEFAULT 0                COMMENT '会员等级(0:普通会员)',
    `points`        INT             DEFAULT 0                COMMENT '积分',
    `reg_time`      DATETIME        DEFAULT CURRENT_TIMESTAMP COMMENT '注册时间',
    `last_login`    DATETIME        DEFAULT NULL             COMMENT '最后登录时间',
    `status`        TINYINT         DEFAULT 1                COMMENT '状态(1:正常 0:禁用)',
    `is_deleted`    TINYINT         DEFAULT 0                COMMENT '逻辑删除(1:已删除)',
    PRIMARY KEY (`user_id`),
    UNIQUE KEY `uk_mobile` (`mobile`),
    UNIQUE KEY `uk_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='会员表';

-- ===============================================
-- 2. 商品分类表（三级分类）
-- ===============================================
DROP TABLE IF EXISTS `goods_category`;
CREATE TABLE `goods_category` (
    `id`            BIGINT          NOT NULL AUTO_INCREMENT  COMMENT '分类ID',
    `name`          VARCHAR(100)    NOT NULL                 COMMENT '分类名称',
    `parent_id`     BIGINT          DEFAULT 0                COMMENT '上级分类ID(0:顶级)',
    `level`         TINYINT         NOT NULL                 COMMENT '层级(1/2/3)',
    `sort_order`    INT             DEFAULT 50               COMMENT '排序(越小越前)',
    `is_show`       TINYINT         DEFAULT 1                COMMENT '是否显示(1:是 0:否)',
    `is_hot`        TINYINT         DEFAULT 0                COMMENT '是否热门(1:是 0:否)',
    `image`         VARCHAR(255)    DEFAULT NULL             COMMENT '分类图片',
    `is_deleted`    TINYINT         DEFAULT 0                COMMENT '逻辑删除',
    PRIMARY KEY (`id`),
    KEY `idx_parent_id` (`parent_id`),
    KEY `idx_level` (`level`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品分类表';

-- ===============================================
-- 3. 品牌表
-- ===============================================
DROP TABLE IF EXISTS `brand`;
CREATE TABLE `brand` (
    `id`            BIGINT          NOT NULL AUTO_INCREMENT  COMMENT '品牌ID',
    `name`          VARCHAR(100)    NOT NULL                 COMMENT '品牌名称',
    `logo`          VARCHAR(255)    DEFAULT NULL             COMMENT '品牌Logo',
    `description`   TEXT            DEFAULT NULL             COMMENT '品牌描述',
    `sort_order`    INT             DEFAULT 50               COMMENT '排序',
    `is_hot`        TINYINT         DEFAULT 0                COMMENT '是否热门',
    `is_deleted`    TINYINT         DEFAULT 0                COMMENT '逻辑删除',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='品牌表';

-- ===============================================
-- 4. 商品表
-- ===============================================
DROP TABLE IF EXISTS `goods`;
CREATE TABLE `goods` (
    `goods_id`      BIGINT          NOT NULL AUTO_INCREMENT  COMMENT '商品ID',
    `goods_sn`      VARCHAR(50)     NOT NULL                 COMMENT '商品编号',
    `goods_name`    VARCHAR(255)    NOT NULL                 COMMENT '商品名称',
    `cat_id`        BIGINT          NOT NULL                 COMMENT '所属分类ID',
    `brand_id`      BIGINT          DEFAULT 0                COMMENT '品牌ID',
    `shop_price`    DECIMAL(10,2)   NOT NULL                 COMMENT '促销价/售价',
    `market_price`  DECIMAL(10,2)   DEFAULT 0.00             COMMENT '市场价/原价',
    `store_count`   INT             DEFAULT 0                COMMENT '库存数量',
    `sales_sum`     INT             DEFAULT 0                COMMENT '销量',
    `keywords`      VARCHAR(255)    DEFAULT NULL             COMMENT 'SEO关键词',
    `goods_content` MEDIUMTEXT      DEFAULT NULL             COMMENT '商品详情(图文)',
    `goods_thumb`   VARCHAR(255)    DEFAULT NULL             COMMENT '商品缩略图',
    `is_on_sale`    TINYINT         DEFAULT 1                COMMENT '是否上架(1:是 0:否)',
    `is_hot`        TINYINT         DEFAULT 0                COMMENT '是否热门',
    `is_recommend`  TINYINT         DEFAULT 0                COMMENT '是否推荐',
    `sort_order`    INT             DEFAULT 50               COMMENT '排序',
    `add_time`      DATETIME        DEFAULT CURRENT_TIMESTAMP COMMENT '添加时间',
    `update_time`   DATETIME        DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    `is_deleted`    TINYINT         DEFAULT 0                COMMENT '逻辑删除',
    PRIMARY KEY (`goods_id`),
    UNIQUE KEY `uk_goods_sn` (`goods_sn`),
    KEY `idx_cat_id` (`cat_id`),
    KEY `idx_is_on_sale` (`is_on_sale`),
    KEY `idx_is_hot` (`is_hot`),
    KEY `idx_is_recommend` (`is_recommend`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品表';

-- ===============================================
-- 5. 商品图片表
-- ===============================================
DROP TABLE IF EXISTS `goods_images`;
CREATE TABLE `goods_images` (
    `img_id`        BIGINT          NOT NULL AUTO_INCREMENT  COMMENT '图片ID',
    `goods_id`      BIGINT          NOT NULL                 COMMENT '商品ID',
    `image_url`     VARCHAR(255)    NOT NULL                 COMMENT '图片URL',
    `sort_order`    INT             DEFAULT 50               COMMENT '排序',
    `is_main`       TINYINT         DEFAULT 0                COMMENT '是否主图(1:是 0:否)',
    PRIMARY KEY (`img_id`),
    KEY `idx_goods_id` (`goods_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品图片表';

-- ===============================================
-- 6. 商品属性/SKU表
-- ===============================================
DROP TABLE IF EXISTS `goods_attr`;
CREATE TABLE `goods_attr` (
    `goods_attr_id` BIGINT          NOT NULL AUTO_INCREMENT  COMMENT '属性ID',
    `goods_id`      BIGINT          NOT NULL                 COMMENT '商品ID',
    `attr_name`     VARCHAR(50)     NOT NULL                 COMMENT '规格名称(如:颜色)',
    `attr_value`    VARCHAR(100)    NOT NULL                 COMMENT '规格值(如:红色)',
    `attr_price`    DECIMAL(10,2)   DEFAULT 0.00             COMMENT '规格差价(可正可负)',
    `store_count`   INT             DEFAULT 0                COMMENT 'SKU库存',
    `is_deleted`    TINYINT         DEFAULT 0                COMMENT '逻辑删除',
    PRIMARY KEY (`goods_attr_id`),
    KEY `idx_goods_id` (`goods_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品属性SKU表';

-- ===============================================
-- 7. 购物车表
-- ===============================================
DROP TABLE IF EXISTS `cart`;
CREATE TABLE `cart` (
    `id`            BIGINT          NOT NULL AUTO_INCREMENT  COMMENT '购物车ID',
    `user_id`       BIGINT          NOT NULL                 COMMENT '用户ID',
    `goods_id`      BIGINT          NOT NULL                 COMMENT '商品ID',
    `goods_attr_id` BIGINT          DEFAULT 0                COMMENT 'SKU属性ID(0:无规格)',
    `goods_num`     INT             NOT NULL DEFAULT 1       COMMENT '购买数量',
    `goods_price`   DECIMAL(10,2)   NOT NULL                 COMMENT '加入时单价',
    `selected`      TINYINT         DEFAULT 1                COMMENT '是否选中(1:是 0:否)',
    `add_time`      DATETIME        DEFAULT CURRENT_TIMESTAMP COMMENT '添加时间',
    PRIMARY KEY (`id`),
    KEY `idx_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='购物车表';

-- ===============================================
-- 8. 订单表
-- ===============================================
DROP TABLE IF EXISTS `order`;
CREATE TABLE `order` (
    `order_id`          BIGINT          NOT NULL AUTO_INCREMENT  COMMENT '订单ID',
    `order_sn`          VARCHAR(50)     NOT NULL                 COMMENT '订单编号',
    `user_id`           BIGINT          NOT NULL                 COMMENT '用户ID',
    `order_status`      VARCHAR(20)     DEFAULT 'PENDING'        COMMENT '订单状态(PENDING/PAID/SHIPPED/COMPLETED/CANCELLED/RETURNING/REFUNDED)',
    `pay_status`        TINYINT         DEFAULT 0                COMMENT '支付状态(0:未支付 1:已支付)',
    `shipping_status`   TINYINT         DEFAULT 0                COMMENT '发货状态(0:未发货 1:已发货 2:已收货)',
    `order_amount`      DECIMAL(10,2)   NOT NULL                 COMMENT '订单总金额',
    `total_amount`      DECIMAL(10,2)   NOT NULL                 COMMENT '商品总金额',
    `shipping_fee`      DECIMAL(10,2)   DEFAULT 0.00             COMMENT '运费',
    `pay_name`          VARCHAR(20)     DEFAULT NULL             COMMENT '支付方式(alipay/wechat/unionpay/cod)',
    `shipping_name`     VARCHAR(20)     DEFAULT NULL             COMMENT '配送方式',
    `pay_time`          DATETIME        DEFAULT NULL             COMMENT '支付时间',
    `shipping_time`     DATETIME        DEFAULT NULL             COMMENT '发货时间',
    `receive_time`      DATETIME        DEFAULT NULL             COMMENT '收货时间',
    `add_time`          DATETIME        DEFAULT CURRENT_TIMESTAMP COMMENT '下单时间',
    `address_snapshot`  JSON            DEFAULT NULL             COMMENT '收货地址快照(JSON)',
    `remark`            VARCHAR(500)    DEFAULT NULL             COMMENT '订单备注',
    `is_deleted`        TINYINT         DEFAULT 0                COMMENT '逻辑删除',
    PRIMARY KEY (`order_id`),
    UNIQUE KEY `uk_order_sn` (`order_sn`),
    KEY `idx_user_id` (`user_id`),
    KEY `idx_order_status` (`order_status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单表';

-- ===============================================
-- 9. 订单商品表
-- ===============================================
DROP TABLE IF EXISTS `order_goods`;
CREATE TABLE `order_goods` (
    `id`            BIGINT          NOT NULL AUTO_INCREMENT  COMMENT 'ID',
    `order_id`      BIGINT          NOT NULL                 COMMENT '订单ID',
    `goods_id`      BIGINT          NOT NULL                 COMMENT '商品ID',
    `goods_name`    VARCHAR(255)    NOT NULL                 COMMENT '商品名称(快照)',
    `goods_price`   DECIMAL(10,2)   NOT NULL                 COMMENT '商品单价(快照)',
    `goods_num`     INT             NOT NULL                 COMMENT '购买数量',
    `goods_image`   VARCHAR(255)    DEFAULT NULL             COMMENT '商品图片(快照)',
    `goods_attr`    VARCHAR(255)    DEFAULT NULL             COMMENT '商品规格(快照)',
    PRIMARY KEY (`id`),
    KEY `idx_order_id` (`order_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单商品表';

-- ===============================================
-- 10. 收货地址表
-- ===============================================
DROP TABLE IF EXISTS `address`;
CREATE TABLE `address` (
    `address_id`    BIGINT          NOT NULL AUTO_INCREMENT  COMMENT '地址ID',
    `user_id`       BIGINT          NOT NULL                 COMMENT '用户ID',
    `consignee`     VARCHAR(50)     NOT NULL                 COMMENT '收货人姓名',
    `mobile`        VARCHAR(20)     NOT NULL                 COMMENT '收货人手机号',
    `province`      VARCHAR(50)     NOT NULL                 COMMENT '省份',
    `city`          VARCHAR(50)     NOT NULL                 COMMENT '城市',
    `district`      VARCHAR(50)     NOT NULL                 COMMENT '区/县',
    `address`       VARCHAR(255)    NOT NULL                 COMMENT '详细地址',
    `is_default`    TINYINT         DEFAULT 0                COMMENT '是否默认地址(1:是 0:否)',
    `is_deleted`    TINYINT         DEFAULT 0                COMMENT '逻辑删除',
    PRIMARY KEY (`address_id`),
    KEY `idx_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='收货地址表';

-- ===============================================
-- 11. 导航表
-- ===============================================
DROP TABLE IF EXISTS `navigation`;
CREATE TABLE `navigation` (
    `id`            BIGINT          NOT NULL AUTO_INCREMENT  COMMENT '导航ID',
    `name`          VARCHAR(50)     NOT NULL                 COMMENT '导航名称',
    `url`           VARCHAR(255)    NOT NULL                 COMMENT '链接地址',
    `sort_order`    INT             DEFAULT 50               COMMENT '排序(越小越前)',
    `is_show`       TINYINT         DEFAULT 1                COMMENT '是否显示(1:是 0:否)',
    `position`      VARCHAR(20)     DEFAULT 'top'            COMMENT '位置(top/main/bottom)',
    `is_deleted`    TINYINT         DEFAULT 0                COMMENT '逻辑删除',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='导航表';

-- ===============================================
-- 12. 广告表
-- ===============================================
DROP TABLE IF EXISTS `ad`;
CREATE TABLE `ad` (
    `ad_id`         BIGINT          NOT NULL AUTO_INCREMENT  COMMENT '广告ID',
    `ad_name`       VARCHAR(100)    NOT NULL                 COMMENT '广告名称',
    `ad_image`      VARCHAR(255)    NOT NULL                 COMMENT '广告图片URL',
    `ad_link`       VARCHAR(255)    DEFAULT NULL             COMMENT '广告链接',
    `position_id`   INT             DEFAULT 0                COMMENT '广告位ID',
    `type`          VARCHAR(20)     DEFAULT 'banner'         COMMENT '广告类型(banner/floor/sidebar)',
    `start_time`    DATETIME        DEFAULT NULL             COMMENT '开始时间',
    `end_time`      DATETIME        DEFAULT NULL             COMMENT '结束时间',
    `enabled`       TINYINT         DEFAULT 1                COMMENT '是否启用(1:是 0:否)',
    `sort_order`    INT             DEFAULT 50               COMMENT '排序',
    `is_deleted`    TINYINT         DEFAULT 0                COMMENT '逻辑删除',
    PRIMARY KEY (`ad_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='广告表';

-- ===============================================
-- 13. 文章表
-- ===============================================
DROP TABLE IF EXISTS `article`;
CREATE TABLE `article` (
    `article_id`    BIGINT          NOT NULL AUTO_INCREMENT  COMMENT '文章ID',
    `title`         VARCHAR(255)    NOT NULL                 COMMENT '文章标题',
    `content`       MEDIUMTEXT      DEFAULT NULL             COMMENT '文章内容',
    `cat_id`        BIGINT          DEFAULT 0                COMMENT '文章分类ID',
    `is_publish`    TINYINT         DEFAULT 1                COMMENT '是否发布(1:是 0:否)',
    `author`        VARCHAR(50)     DEFAULT NULL             COMMENT '作者',
    `publish_time`  DATETIME        DEFAULT CURRENT_TIMESTAMP COMMENT '发布时间',
    `is_deleted`    TINYINT         DEFAULT 0                COMMENT '逻辑删除',
    PRIMARY KEY (`article_id`),
    KEY `idx_cat_id` (`cat_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='文章表';

-- ===============================================
-- 14. 促销表
-- ===============================================
DROP TABLE IF EXISTS `promotion`;
CREATE TABLE `promotion` (
    `id`            BIGINT          NOT NULL AUTO_INCREMENT  COMMENT '促销ID',
    `name`          VARCHAR(100)    NOT NULL                 COMMENT '促销名称',
    `type`          VARCHAR(20)     NOT NULL                 COMMENT '促销类型(满减/打折/优惠券/秒杀)',
    `start_time`    DATETIME        NOT NULL                 COMMENT '开始时间',
    `end_time`      DATETIME        NOT NULL                 COMMENT '结束时间',
    `rules`         JSON            DEFAULT NULL             COMMENT '促销规则(JSON)',
    `is_enabled`    TINYINT         DEFAULT 1                COMMENT '是否启用',
    `description`   TEXT            DEFAULT NULL             COMMENT '促销描述',
    `is_deleted`    TINYINT         DEFAULT 0                COMMENT '逻辑删除',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='促销表';

-- ===============================================
-- 15. 管理员表
-- ===============================================
DROP TABLE IF EXISTS `admin`;
CREATE TABLE `admin` (
    `admin_id`      BIGINT          NOT NULL AUTO_INCREMENT  COMMENT '管理员ID',
    `username`      VARCHAR(50)     NOT NULL                 COMMENT '用户名',
    `password`      VARCHAR(255)    NOT NULL                 COMMENT '密码(BCrypt加密)',
    `real_name`     VARCHAR(50)     DEFAULT NULL             COMMENT '真实姓名',
    `role_id`       BIGINT          DEFAULT 0                COMMENT '角色ID',
    `status`        TINYINT         DEFAULT 1                COMMENT '状态(1:正常 0:禁用)',
    `last_login`    DATETIME        DEFAULT NULL             COMMENT '最后登录时间',
    `is_deleted`    TINYINT         DEFAULT 0                COMMENT '逻辑删除',
    PRIMARY KEY (`admin_id`),
    UNIQUE KEY `uk_username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='管理员表';

-- ===============================================
-- 16. 管理员角色表
-- ===============================================
DROP TABLE IF EXISTS `admin_role`;
CREATE TABLE `admin_role` (
    `role_id`       BIGINT          NOT NULL AUTO_INCREMENT  COMMENT '角色ID',
    `role_name`     VARCHAR(50)     NOT NULL                 COMMENT '角色名称',
    `description`   VARCHAR(255)    DEFAULT NULL             COMMENT '角色描述',
    `permissions`   JSON            DEFAULT NULL             COMMENT '权限列表(JSON)',
    `status`        TINYINT         DEFAULT 1                COMMENT '状态(1:正常 0:禁用)',
    `is_deleted`    TINYINT         DEFAULT 0                COMMENT '逻辑删除',
    PRIMARY KEY (`role_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='管理员角色表';

-- ===============================================
-- 17. 系统菜单/权限表
-- ===============================================
DROP TABLE IF EXISTS `system_menu`;
CREATE TABLE `system_menu` (
    `id`            BIGINT          NOT NULL AUTO_INCREMENT  COMMENT '菜单ID',
    `name`          VARCHAR(50)     NOT NULL                 COMMENT '菜单名称',
    `url`           VARCHAR(255)    DEFAULT NULL             COMMENT '菜单URL',
    `parent_id`     BIGINT          DEFAULT 0                COMMENT '上级菜单ID',
    `icon`          VARCHAR(50)     DEFAULT NULL             COMMENT '图标',
    `sort_order`    INT             DEFAULT 50               COMMENT '排序',
    `type`          VARCHAR(10)     DEFAULT 'menu'           COMMENT '类型(menu:菜单 button:按钮)',
    `is_deleted`    TINYINT         DEFAULT 0                COMMENT '逻辑删除',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='系统菜单表';

-- ===============================================
-- 18. 系统配置表
-- ===============================================
DROP TABLE IF EXISTS `config`;
CREATE TABLE `config` (
    `id`            BIGINT          NOT NULL AUTO_INCREMENT  COMMENT '配置ID',
    `config_key`    VARCHAR(100)    NOT NULL                 COMMENT '配置键名',
    `config_value`  TEXT            DEFAULT NULL             COMMENT '配置值',
    `description`   VARCHAR(255)    DEFAULT NULL             COMMENT '配置说明',
    `group_name`    VARCHAR(50)     DEFAULT 'basic'          COMMENT '配置分组',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_config_key` (`config_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='系统配置表';
