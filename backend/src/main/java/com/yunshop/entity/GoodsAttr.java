package com.yunshop.entity;

import com.baomidou.mybatisplus.annotation.*;
import java.math.BigDecimal;

/**
 * 商品属性/SKU实体 (goods_attr 表)
 */
@TableName("goods_attr")
public class GoodsAttr {

    @TableId(type = IdType.AUTO)
    private Long goodsAttrId;

    private Long goodsId;

    private String attrName;

    private String attrValue;

    private BigDecimal attrPrice;

    private Integer storeCount;

    @TableLogic
    private Integer isDeleted;

    // getters/setters
    public Long getGoodsAttrId() { return goodsAttrId; }
    public void setGoodsAttrId(Long goodsAttrId) { this.goodsAttrId = goodsAttrId; }
    public Long getGoodsId() { return goodsId; }
    public void setGoodsId(Long goodsId) { this.goodsId = goodsId; }
    public String getAttrName() { return attrName; }
    public void setAttrName(String attrName) { this.attrName = attrName; }
    public String getAttrValue() { return attrValue; }
    public void setAttrValue(String attrValue) { this.attrValue = attrValue; }
    public BigDecimal getAttrPrice() { return attrPrice; }
    public void setAttrPrice(BigDecimal attrPrice) { this.attrPrice = attrPrice; }
    public Integer getStoreCount() { return storeCount; }
    public void setStoreCount(Integer storeCount) { this.storeCount = storeCount; }
    public Integer getIsDeleted() { return isDeleted; }
    public void setIsDeleted(Integer isDeleted) { this.isDeleted = isDeleted; }
}
