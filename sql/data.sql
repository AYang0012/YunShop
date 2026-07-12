-- ===============================================
-- 云集优选 B2C 电商平台 - 初始测试数据
-- ===============================================

USE yunshop;

-- ===============================================
-- 管理员数据（密码: admin123）
-- ===============================================
INSERT INTO `admin` (`admin_id`, `username`, `password`, `real_name`, `role_id`, `status`) VALUES
(1, 'admin', '$2a$10$N.zmdr9k7uOCQb376NoUnuTJ8iAt6Z5EHsM8lE9lBOsl7iAt6Z5Eh', '超级管理员', 1, 1);

-- ===============================================
-- 管理员角色
-- ===============================================
INSERT INTO `admin_role` (`role_id`, `role_name`, `description`, `permissions`, `status`) VALUES
(1, '超级管理员', '拥有所有权限', '{"all": true}', 1),
(2, '仓管员', '仓库管理与库存管理', '{"goods": ["view","edit"], "order": ["view"]}', 1),
(3, '客服', '订单处理、发货、退换货', '{"order": ["view","edit","ship","refund"]}', 1);

-- ===============================================
-- 系统菜单
-- ===============================================
INSERT INTO `system_menu` (`id`, `name`, `url`, `parent_id`, `icon`, `sort_order`, `type`) VALUES
(1, '系统设置', '/admin/system', 0, 'gear', 10, 'menu'),
(2, '商品管理', '/admin/goods', 0, 'box', 20, 'menu'),
(3, '订单管理', '/admin/order', 0, 'list-check', 30, 'menu'),
(4, '会员管理', '/admin/user', 0, 'people', 40, 'menu'),
(5, '广告管理', '/admin/ad', 0, 'image', 50, 'menu'),
(6, '文章管理', '/admin/article', 0, 'file-text', 60, 'menu'),
(7, '品牌管理', '/admin/brand', 0, 'tag', 70, 'menu'),
(8, '导航管理', '/admin/navigation', 0, 'link', 80, 'menu'),
(9, '促销管理', '/admin/promotion', 0, 'gift', 90, 'menu');

-- ===============================================
-- 导航数据
-- ===============================================
INSERT INTO `navigation` (`id`, `name`, `url`, `sort_order`, `is_show`, `position`) VALUES
(1, '首页', '/', 10, 1, 'top'),
(2, '手机数码', '/goods/list?catId=1', 20, 1, 'top'),
(3, '电脑办公', '/goods/list?catId=2', 30, 1, 'top'),
(4, '家用电器', '/goods/list?catId=3', 40, 1, 'top'),
(5, '服装鞋帽', '/goods/list?catId=4', 50, 1, 'top'),
(6, '食品生鲜', '/goods/list?catId=5', 60, 1, 'top'),
(7, '美妆个护', '/goods/list?catId=6', 70, 1, 'top'),
(8, '帮助中心', '/article/list', 80, 1, 'top');

-- ===============================================
-- 商品分类（三级）
-- ===============================================
INSERT INTO `goods_category` (`id`, `name`, `parent_id`, `level`, `sort_order`, `is_show`, `is_hot`) VALUES
-- 一级分类
(1, '手机数码', 0, 1, 10, 1, 1),
(2, '电脑办公', 0, 1, 20, 1, 1),
(3, '家用电器', 0, 1, 30, 1, 1),
(4, '服装鞋帽', 0, 1, 40, 1, 1),
(5, '食品生鲜', 0, 1, 50, 1, 1),
(6, '美妆个护', 0, 1, 60, 1, 0),
-- 手机数码二级
(11, '手机', 1, 2, 10, 1, 0),
(12, '平板电脑', 1, 2, 20, 1, 0),
(13, '数码配件', 1, 2, 30, 1, 0),
-- 手机数码三级
(111, '智能手机', 11, 3, 10, 1, 0),
(112, '老人手机', 11, 3, 20, 1, 0),
(121, 'Android平板', 12, 3, 10, 1, 0),
(122, 'iPad', 12, 3, 20, 1, 0),
(131, '充电器', 13, 3, 10, 1, 0),
(132, '数据线', 13, 3, 20, 1, 0),
-- 电脑办公二级
(21, '笔记本', 2, 2, 10, 1, 0),
(22, '台式机', 2, 2, 20, 1, 0),
(23, '办公设备', 2, 2, 30, 1, 0),
-- 家用电器二级
(31, '空调', 3, 2, 10, 1, 0),
(32, '洗衣机', 3, 2, 20, 1, 0),
(33, '冰箱', 3, 2, 30, 1, 0),
-- 服装鞋帽二级
(41, '男装', 4, 2, 10, 1, 0),
(42, '女装', 4, 2, 20, 1, 0),
(43, '鞋靴', 4, 2, 30, 1, 0),
-- 食品生鲜二级
(51, '水果', 5, 2, 10, 1, 0),
(52, '蔬菜', 5, 2, 20, 1, 0),
(53, '肉类', 5, 2, 30, 1, 0),
-- 美妆个护二级
(61, '护肤', 6, 2, 10, 1, 0),
(62, '彩妆', 6, 2, 20, 1, 0);

-- ===============================================
-- 品牌数据
-- ===============================================
INSERT INTO `brand` (`id`, `name`, `description`, `sort_order`, `is_hot`) VALUES
(1, '华为', '华为技术有限公司', 10, 1),
(2, '苹果', 'Apple Inc.', 20, 1),
(3, '小米', '小米科技有限公司', 30, 1),
(4, '联想', '联想集团', 40, 1),
(5, '格力', '格力电器', 50, 1),
(6, '海尔', '海尔集团', 60, 1);

-- ===============================================
-- 示例商品
-- ===============================================
INSERT INTO `goods` (`goods_id`, `goods_sn`, `goods_name`, `cat_id`, `brand_id`, `shop_price`, `market_price`, `store_count`, `sales_sum`, `keywords`, `goods_content`, `goods_thumb`, `is_on_sale`, `is_hot`, `is_recommend`) VALUES
(1, 'SN20260601001', '华为Mate 60 Pro 智能手机 5G全网通', 111, 1, 6999.00, 7999.00, 100, 256, '华为,Mate60,5G', '<p>华为Mate 60 Pro 旗舰手机</p>', '/upload/goods/1.jpg', 1, 1, 1),
(2, 'SN20260601002', 'iPhone 15 Pro Max 256GB', 111, 2, 8999.00, 9999.00, 80, 189, 'iPhone,苹果', '<p>iPhone 15 Pro Max</p>', '/upload/goods/2.jpg', 1, 1, 1),
(3, 'SN20260601003', '小米14 Ultra 影像旗舰', 111, 3, 5999.00, 6499.00, 150, 312, '小米,14,Ultra', '<p>小米14 Ultra 拍照旗舰</p>', '/upload/goods/3.jpg', 1, 1, 1),
(4, 'SN20260601004', '联想ThinkPad X1 Carbon 商务本', 21, 4, 9999.00, 12999.00, 50, 89, 'ThinkPad,联想,商务', '<p>ThinkPad X1 Carbon 轻薄商务笔记本</p>', '/upload/goods/4.jpg', 1, 1, 1),
(5, 'SN20260601005', 'Apple MacBook Pro 14英寸', 21, 2, 14999.00, 16999.00, 40, 67, 'MacBook,苹果', '<p>MacBook Pro M3芯片</p>', '/upload/goods/5.jpg', 1, 1, 1),
(6, 'SN20260601006', '格力空调 1.5匹 变频冷暖', 31, 5, 3299.00, 3999.00, 200, 432, '格力,空调,变频', '<p>格力1.5匹变频空调</p>', '/upload/goods/6.jpg', 1, 1, 1),
(7, 'SN20260601007', '海尔双门冰箱 500L 风冷无霜', 33, 6, 4599.00, 5299.00, 60, 123, '海尔,冰箱', '<p>海尔大容量冰箱</p>', '/upload/goods/7.jpg', 1, 1, 0),
(8, 'SN20260601008', '小米平板6 Pro 11英寸', 121, 3, 2499.00, 2799.00, 120, 198, '小米,平板', '<p>小米平板6 Pro</p>', '/upload/goods/8.jpg', 1, 0, 1),
(9, 'SN20260601009', '华为MatePad Pro 12.6英寸', 121, 1, 4299.00, 4999.00, 70, 145, '华为,平板', '<p>华为MatePad Pro旗舰平板</p>', '/upload/goods/9.jpg', 1, 0, 1),
(10, 'SN20260601010', '65W氮化镓充电器 多口快充', 131, 3, 89.00, 129.00, 500, 1024, '充电器,快充', '<p>65W高速充电器</p>', '/upload/goods/10.jpg', 1, 0, 1);

-- ===============================================
-- 商品图片（每个商品一张默认图）
-- ===============================================
INSERT INTO `goods_images` (`img_id`, `goods_id`, `image_url`, `sort_order`, `is_main`) VALUES
(1, 1, '/upload/goods/1.jpg', 10, 1),
(2, 2, '/upload/goods/2.jpg', 10, 1),
(3, 3, '/upload/goods/3.jpg', 10, 1),
(4, 4, '/upload/goods/4.jpg', 10, 1),
(5, 5, '/upload/goods/5.jpg', 10, 1),
(6, 6, '/upload/goods/6.jpg', 10, 1),
(7, 7, '/upload/goods/7.jpg', 10, 1),
(8, 8, '/upload/goods/8.jpg', 10, 1),
(9, 9, '/upload/goods/9.jpg', 10, 1),
(10, 10, '/upload/goods/10.jpg', 10, 1);

-- ===============================================
-- 广告数据（Banner）
-- ===============================================
INSERT INTO `ad` (`ad_id`, `ad_name`, `ad_image`, `ad_link`, `position_id`, `type`, `enabled`, `sort_order`) VALUES
(1, '华为Mate60', '/upload/goods/1.jpg', '/goods/detail/1', 1, 'banner', 1, 10),
(2, 'iPhone15', '/upload/goods/2.jpg', '/goods/detail/2', 1, 'banner', 1, 20),
(3, '小米14', '/upload/goods/3.jpg', '/goods/detail/3', 1, 'banner', 1, 30);

-- ===============================================
-- 系统配置
-- ===============================================
INSERT INTO `config` (`id`, `config_key`, `config_value`, `description`, `group_name`) VALUES
(1, 'site_name', '云集优选', '网站名称', 'basic'),
(2, 'site_logo', '/static/images/logo.png', '网站Logo', 'basic'),
(3, 'site_keywords', '云集优选,B2C,电商', 'SEO关键词', 'basic'),
(4, 'site_description', '云集优选 - 品质生活，尽在云集', '网站描述', 'basic'),
(5, 'site_icp', '京ICP备XXXXXXXX号', '备案号', 'basic');
