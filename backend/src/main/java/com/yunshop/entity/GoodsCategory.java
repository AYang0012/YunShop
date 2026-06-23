package com.yunshop.entity;

import com.baomidou.mybatisplus.annotation.*;

/**
 * 商品分类实体 (goods_category 表)
 */
@TableName("goods_category")
public class GoodsCategory {

    @TableId(type = IdType.AUTO)
    private Long id;

    private String name;

    private Long parentId;

    private Integer level;

    private Integer sortOrder;

    private Integer isShow;

    private Integer isHot;

    private String image;

    @TableLogic
    private Integer isDeleted;

    // getters/setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public Long getParentId() { return parentId; }
    public void setParentId(Long parentId) { this.parentId = parentId; }
    public Integer getLevel() { return level; }
    public void setLevel(Integer level) { this.level = level; }
    public Integer getSortOrder() { return sortOrder; }
    public void setSortOrder(Integer sortOrder) { this.sortOrder = sortOrder; }
    public Integer getIsShow() { return isShow; }
    public void setIsShow(Integer isShow) { this.isShow = isShow; }
    public Integer getIsHot() { return isHot; }
    public void setIsHot(Integer isHot) { this.isHot = isHot; }
    public String getImage() { return image; }
    public void setImage(String image) { this.image = image; }
    public Integer getIsDeleted() { return isDeleted; }
    public void setIsDeleted(Integer isDeleted) { this.isDeleted = isDeleted; }
}
