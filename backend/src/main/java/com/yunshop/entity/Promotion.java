package com.yunshop.entity;

import com.baomidou.mybatisplus.annotation.*;
import java.time.LocalDateTime;

/**
 * 促销实体 (promotion 表)
 */
@TableName("promotion")
public class Promotion {

    @TableId(type = IdType.AUTO)
    private Long id;

    private String name;

    private String type;

    private LocalDateTime startTime;

    private LocalDateTime endTime;

    private String rules;

    private Integer isEnabled;

    private String description;

    @TableLogic
    private Integer isDeleted;

    // getters/setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getType() { return type; }
    public void setType(String type) { this.type = type; }
    public LocalDateTime getStartTime() { return startTime; }
    public void setStartTime(LocalDateTime startTime) { this.startTime = startTime; }
    public LocalDateTime getEndTime() { return endTime; }
    public void setEndTime(LocalDateTime endTime) { this.endTime = endTime; }
    public String getRules() { return rules; }
    public void setRules(String rules) { this.rules = rules; }
    public Integer getIsEnabled() { return isEnabled; }
    public void setIsEnabled(Integer isEnabled) { this.isEnabled = isEnabled; }
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
    public Integer getIsDeleted() { return isDeleted; }
    public void setIsDeleted(Integer isDeleted) { this.isDeleted = isDeleted; }
}
