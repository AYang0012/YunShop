package com.yunshop.entity;

import com.baomidou.mybatisplus.annotation.*;
import java.math.BigDecimal;

/**
 * 订单商品实体 (order_goods 表)
 */
@TableName("order_goods")
public class OrderGoods {

    @TableId(type = IdType.AUTO)
    private Long id;

    private Long orderId;

    private Long goodsId;

    private String goodsName;

    private BigDecimal goodsPrice;

    private Integer goodsNum;

    private String goodsImage;

    private String goodsAttr;

    // getters/setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public Long getOrderId() { return orderId; }
    public void setOrderId(Long orderId) { this.orderId = orderId; }
    public Long getGoodsId() { return goodsId; }
    public void setGoodsId(Long goodsId) { this.goodsId = goodsId; }
    public String getGoodsName() { return goodsName; }
    public void setGoodsName(String goodsName) { this.goodsName = goodsName; }
    public BigDecimal getGoodsPrice() { return goodsPrice; }
    public void setGoodsPrice(BigDecimal goodsPrice) { this.goodsPrice = goodsPrice; }
    public Integer getGoodsNum() { return goodsNum; }
    public void setGoodsNum(Integer goodsNum) { this.goodsNum = goodsNum; }
    public String getGoodsImage() { return goodsImage; }
    public void setGoodsImage(String goodsImage) { this.goodsImage = goodsImage; }
    public String getGoodsAttr() { return goodsAttr; }
    public void setGoodsAttr(String goodsAttr) { this.goodsAttr = goodsAttr; }
}
