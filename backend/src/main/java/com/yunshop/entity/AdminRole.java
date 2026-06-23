package com.yunshop.entity;

import com.baomidou.mybatisplus.annotation.*;

/**
 * 管理员角色实体 (admin_role 表)
 */
@TableName("admin_role")
public class AdminRole {

    @TableId(type = IdType.AUTO)
    private Long roleId;

    private String roleName;

    private String description;

    private String permissions;

    private Integer status;

    @TableLogic
    private Integer isDeleted;

    // getters/setters
    public Long getRoleId() { return roleId; }
    public void setRoleId(Long roleId) { this.roleId = roleId; }
    public String getRoleName() { return roleName; }
    public void setRoleName(String roleName) { this.roleName = roleName; }
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
    public String getPermissions() { return permissions; }
    public void setPermissions(String permissions) { this.permissions = permissions; }
    public Integer getStatus() { return status; }
    public void setStatus(Integer status) { this.status = status; }
    public Integer getIsDeleted() { return isDeleted; }
    public void setIsDeleted(Integer isDeleted) { this.isDeleted = isDeleted; }
}
