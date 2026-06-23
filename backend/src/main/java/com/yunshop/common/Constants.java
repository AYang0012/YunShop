package com.yunshop.common;

/**
 * 系统常量
 */
public class Constants {

    /** Session 中存储前台用户的 key */
    public static final String SESSION_USER = "frontUser";

    /** Session 中存储后台管理员的 key */
    public static final String SESSION_ADMIN = "adminUser";

    /** 验证码 Session key */
    public static final String SESSION_CAPTCHA = "captcha";

    /** 购物车最大商品种类 */
    public static final int CART_MAX_TYPES = 20;

    /** 购物车单品最大数量 */
    public static final int CART_MAX_QUANTITY = 200;

    /** 购物车单品最小数量 */
    public static final int CART_MIN_QUANTITY = 1;

    /** 收货地址最大数量 */
    public static final int ADDRESS_MAX_COUNT = 20;

    /** 默认每页条数 */
    public static final int DEFAULT_PAGE_SIZE = 12;

    /** 订单状态 */
    public static final String ORDER_PENDING = "PENDING";       // 待付款
    public static final String ORDER_PAID = "PAID";             // 已付款
    public static final String ORDER_SHIPPED = "SHIPPED";       // 已发货
    public static final String ORDER_COMPLETED = "COMPLETED";   // 已完成
    public static final String ORDER_CANCELLED = "CANCELLED";   // 已取消
    public static final String ORDER_RETURNING = "RETURNING";   // 退货中
    public static final String ORDER_REFUNDED = "REFUNDED";     // 已退款

    /** 支付方式 */
    public static final String PAY_ALIPAY = "alipay";
    public static final String PAY_WECHAT = "wechat";
    public static final String PAY_UNIONPAY = "unionpay";
    public static final String PAY_COD = "cod";                 // 货到付款
}
