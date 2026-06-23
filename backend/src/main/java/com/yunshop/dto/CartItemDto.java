package com.yunshop.dto;

import java.math.BigDecimal;

/**
 * 购物车展示 DTO（关联查询结果）
 */
public class CartItemDto {

    private Long cartId;
    private Long goodsId;
    private String goodsName;
    private String goodsThumb;
    private BigDecimal goodsPrice;
    private Integer goodsNum;
    private BigDecimal subtotal;        // 小计
    private Integer selected;
    private Integer storeCount;         // 库存
    private String attrInfo;            // 规格信息

    public Long getCartId() { return cartId; }
    public void setCartId(Long cartId) { this.cartId = cartId; }
    public Long getGoodsId() { return goodsId; }
    public void setGoodsId(Long goodsId) { this.goodsId = goodsId; }
    public String getGoodsName() { return goodsName; }
    public void setGoodsName(String goodsName) { this.goodsName = goodsName; }
    public String getGoodsThumb() { return goodsThumb; }
    public void setGoodsThumb(String goodsThumb) { this.goodsThumb = goodsThumb; }
    public BigDecimal getGoodsPrice() { return goodsPrice; }
    public void setGoodsPrice(BigDecimal goodsPrice) { this.goodsPrice = goodsPrice; }
    public Integer getGoodsNum() { return goodsNum; }
    public void setGoodsNum(Integer goodsNum) { this.goodsNum = goodsNum; }
    public BigDecimal getSubtotal() { return subtotal; }
    public void setSubtotal(BigDecimal subtotal) { this.subtotal = subtotal; }
    public Integer getSelected() { return selected; }
    public void setSelected(Integer selected) { this.selected = selected; }
    public Integer getStoreCount() { return storeCount; }
    public void setStoreCount(Integer storeCount) { this.storeCount = storeCount; }
    public String getAttrInfo() { return attrInfo; }
    public void setAttrInfo(String attrInfo) { this.attrInfo = attrInfo; }
}
