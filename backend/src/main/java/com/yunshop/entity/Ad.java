package com.yunshop.entity;

import com.baomidou.mybatisplus.annotation.*;
import java.time.LocalDateTime;

/**
 * 广告实体 (ad 表)
 */
@TableName("ad")
public class Ad {

    @TableId(type = IdType.AUTO)
    private Long adId;

    private String adName;

    private String adImage;

    private String adLink;

    private Integer positionId;

    private String type;

    private LocalDateTime startTime;

    private LocalDateTime endTime;

    private Integer enabled;

    private Integer sortOrder;

    @TableLogic
    private Integer isDeleted;

    // getters/setters
    public Long getAdId() { return adId; }
    public void setAdId(Long adId) { this.adId = adId; }
    public String getAdName() { return adName; }
    public void setAdName(String adName) { this.adName = adName; }
    public String getAdImage() { return adImage; }
    public void setAdImage(String adImage) { this.adImage = adImage; }
    public String getAdLink() { return adLink; }
    public void setAdLink(String adLink) { this.adLink = adLink; }
    public Integer getPositionId() { return positionId; }
    public void setPositionId(Integer positionId) { this.positionId = positionId; }
    public String getType() { return type; }
    public void setType(String type) { this.type = type; }
    public LocalDateTime getStartTime() { return startTime; }
    public void setStartTime(LocalDateTime startTime) { this.startTime = startTime; }
    public LocalDateTime getEndTime() { return endTime; }
    public void setEndTime(LocalDateTime endTime) { this.endTime = endTime; }
    public Integer getEnabled() { return enabled; }
    public void setEnabled(Integer enabled) { this.enabled = enabled; }
    public Integer getSortOrder() { return sortOrder; }
    public void setSortOrder(Integer sortOrder) { this.sortOrder = sortOrder; }
    public Integer getIsDeleted() { return isDeleted; }
    public void setIsDeleted(Integer isDeleted) { this.isDeleted = isDeleted; }
}
