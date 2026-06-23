package com.yunshop.entity;

import com.baomidou.mybatisplus.annotation.*;

/**
 * 导航实体 (navigation 表)
 */
@TableName("navigation")
public class Navigation {

    @TableId(type = IdType.AUTO)
    private Long id;

    private String name;

    private String url;

    private Integer sortOrder;

    private Integer isShow;

    private String position;

    @TableLogic
    private Integer isDeleted;

    // getters/setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getUrl() { return url; }
    public void setUrl(String url) { this.url = url; }
    public Integer getSortOrder() { return sortOrder; }
    public void setSortOrder(Integer sortOrder) { this.sortOrder = sortOrder; }
    public Integer getIsShow() { return isShow; }
    public void setIsShow(Integer isShow) { this.isShow = isShow; }
    public String getPosition() { return position; }
    public void setPosition(String position) { this.position = position; }
    public Integer getIsDeleted() { return isDeleted; }
    public void setIsDeleted(Integer isDeleted) { this.isDeleted = isDeleted; }
}
