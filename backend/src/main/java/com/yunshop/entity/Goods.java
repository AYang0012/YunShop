package com.yunshop.entity;

import com.baomidou.mybatisplus.annotation.*;
import java.math.BigDecimal;
import java.time.LocalDateTime;

/**
 * 商品实体 (goods 表)
 */
@TableName("goods")
public class Goods {

    @TableId(type = IdType.AUTO)
    private Long goodsId;

    private String goodsSn;

    private String goodsName;

    private Long catId;

    private Long brandId;

    private BigDecimal shopPrice;

    private BigDecimal marketPrice;

    private Integer storeCount;

    private Integer salesSum;

    private String keywords;

    private String goodsContent;

    private String goodsThumb;

    private Integer isOnSale;

    private Integer isHot;

    private Integer isRecommend;

    private Integer sortOrder;

    private LocalDateTime addTime;

    private LocalDateTime updateTime;

    @TableLogic
    private Integer isDeleted;

    // getters/setters
    public Long getGoodsId() { return goodsId; }
    public void setGoodsId(Long goodsId) { this.goodsId = goodsId; }
    public String getGoodsSn() { return goodsSn; }
    public void setGoodsSn(String goodsSn) { this.goodsSn = goodsSn; }
    public String getGoodsName() { return goodsName; }
    public void setGoodsName(String goodsName) { this.goodsName = goodsName; }
    public Long getCatId() { return catId; }
    public void setCatId(Long catId) { this.catId = catId; }
    public Long getBrandId() { return brandId; }
    public void setBrandId(Long brandId) { this.brandId = brandId; }
    public BigDecimal getShopPrice() { return shopPrice; }
    public void setShopPrice(BigDecimal shopPrice) { this.shopPrice = shopPrice; }
    public BigDecimal getMarketPrice() { return marketPrice; }
    public void setMarketPrice(BigDecimal marketPrice) { this.marketPrice = marketPrice; }
    public Integer getStoreCount() { return storeCount; }
    public void setStoreCount(Integer storeCount) { this.storeCount = storeCount; }
    public Integer getSalesSum() { return salesSum; }
    public void setSalesSum(Integer salesSum) { this.salesSum = salesSum; }
    public String getKeywords() { return keywords; }
    public void setKeywords(String keywords) { this.keywords = keywords; }
    public String getGoodsContent() { return goodsContent; }
    public void setGoodsContent(String goodsContent) { this.goodsContent = goodsContent; }
    public String getGoodsThumb() { return goodsThumb; }
    public void setGoodsThumb(String goodsThumb) { this.goodsThumb = goodsThumb; }
    public Integer getIsOnSale() { return isOnSale; }
    public void setIsOnSale(Integer isOnSale) { this.isOnSale = isOnSale; }
    public Integer getIsHot() { return isHot; }
    public void setIsHot(Integer isHot) { this.isHot = isHot; }
    public Integer getIsRecommend() { return isRecommend; }
    public void setIsRecommend(Integer isRecommend) { this.isRecommend = isRecommend; }
    public Integer getSortOrder() { return sortOrder; }
    public void setSortOrder(Integer sortOrder) { this.sortOrder = sortOrder; }
    public LocalDateTime getAddTime() { return addTime; }
    public void setAddTime(LocalDateTime addTime) { this.addTime = addTime; }
    public LocalDateTime getUpdateTime() { return updateTime; }
    public void setUpdateTime(LocalDateTime updateTime) { this.updateTime = updateTime; }
    public Integer getIsDeleted() { return isDeleted; }
    public void setIsDeleted(Integer isDeleted) { this.isDeleted = isDeleted; }
}
