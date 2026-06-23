package com.yunshop.entity;

import com.baomidou.mybatisplus.annotation.*;

/**
 * 商品图片实体 (goods_images 表)
 */
@TableName("goods_images")
public class GoodsImage {

    @TableId(type = IdType.AUTO)
    private Long imgId;

    private Long goodsId;

    private String imageUrl;

    private Integer sortOrder;

    private Integer isMain;

    // getters/setters
    public Long getImgId() { return imgId; }
    public void setImgId(Long imgId) { this.imgId = imgId; }
    public Long getGoodsId() { return goodsId; }
    public void setGoodsId(Long goodsId) { this.goodsId = goodsId; }
    public String getImageUrl() { return imageUrl; }
    public void setImageUrl(String imageUrl) { this.imageUrl = imageUrl; }
    public Integer getSortOrder() { return sortOrder; }
    public void setSortOrder(Integer sortOrder) { this.sortOrder = sortOrder; }
    public Integer getIsMain() { return isMain; }
    public void setIsMain(Integer isMain) { this.isMain = isMain; }
}
