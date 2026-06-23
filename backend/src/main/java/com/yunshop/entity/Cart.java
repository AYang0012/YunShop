package com.yunshop.entity;

import com.baomidou.mybatisplus.annotation.*;
import java.math.BigDecimal;
import java.time.LocalDateTime;

/**
 * 购物车实体 (cart 表)
 */
@TableName("cart")
public class Cart {

    @TableId(type = IdType.AUTO)
    private Long id;

    private Long userId;

    private Long goodsId;

    private Long goodsAttrId;

    private Integer goodsNum;

    private BigDecimal goodsPrice;

    private Integer selected;

    private LocalDateTime addTime;

    // getters/setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public Long getUserId() { return userId; }
    public void setUserId(Long userId) { this.userId = userId; }
    public Long getGoodsId() { return goodsId; }
    public void setGoodsId(Long goodsId) { this.goodsId = goodsId; }
    public Long getGoodsAttrId() { return goodsAttrId; }
    public void setGoodsAttrId(Long goodsAttrId) { this.goodsAttrId = goodsAttrId; }
    public Integer getGoodsNum() { return goodsNum; }
    public void setGoodsNum(Integer goodsNum) { this.goodsNum = goodsNum; }
    public BigDecimal getGoodsPrice() { return goodsPrice; }
    public void setGoodsPrice(BigDecimal goodsPrice) { this.goodsPrice = goodsPrice; }
    public Integer getSelected() { return selected; }
    public void setSelected(Integer selected) { this.selected = selected; }
    public LocalDateTime getAddTime() { return addTime; }
    public void setAddTime(LocalDateTime addTime) { this.addTime = addTime; }
}
