package com.yunshop.entity;

import com.baomidou.mybatisplus.annotation.*;

/**
 * 系统菜单实体 (system_menu 表)
 */
@TableName("system_menu")
public class SystemMenu {

    @TableId(type = IdType.AUTO)
    private Long id;

    private String name;

    private String url;

    private Long parentId;

    private String icon;

    private Integer sortOrder;

    private String type;

    @TableLogic
    private Integer isDeleted;

    // getters/setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getUrl() { return url; }
    public void setUrl(String url) { this.url = url; }
    public Long getParentId() { return parentId; }
    public void setParentId(Long parentId) { this.parentId = parentId; }
    public String getIcon() { return icon; }
    public void setIcon(String icon) { this.icon = icon; }
    public Integer getSortOrder() { return sortOrder; }
    public void setSortOrder(Integer sortOrder) { this.sortOrder = sortOrder; }
    public String getType() { return type; }
    public void setType(String type) { this.type = type; }
    public Integer getIsDeleted() { return isDeleted; }
    public void setIsDeleted(Integer isDeleted) { this.isDeleted = isDeleted; }
}
