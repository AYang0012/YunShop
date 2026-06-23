package com.yunshop.entity;

import com.baomidou.mybatisplus.annotation.*;

/**
 * 品牌实体 (brand 表)
 */
@TableName("brand")
public class Brand {

    @TableId(type = IdType.AUTO)
    private Long id;

    private String name;

    private String logo;

    private String description;

    private Integer sortOrder;

    private Integer isHot;

    @TableLogic
    private Integer isDeleted;

    // getters/setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getLogo() { return logo; }
    public void setLogo(String logo) { this.logo = logo; }
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
    public Integer getSortOrder() { return sortOrder; }
    public void setSortOrder(Integer sortOrder) { this.sortOrder = sortOrder; }
    public Integer getIsHot() { return isHot; }
    public void setIsHot(Integer isHot) { this.isHot = isHot; }
    public Integer getIsDeleted() { return isDeleted; }
    public void setIsDeleted(Integer isDeleted) { this.isDeleted = isDeleted; }
}
