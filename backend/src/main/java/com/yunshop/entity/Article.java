package com.yunshop.entity;

import com.baomidou.mybatisplus.annotation.*;
import java.time.LocalDateTime;

/**
 * 文章实体 (article 表)
 */
@TableName("article")
public class Article {

    @TableId(type = IdType.AUTO)
    private Long articleId;

    private String title;

    private String content;

    private Long catId;

    private Integer isPublish;

    private String author;

    private LocalDateTime publishTime;

    @TableLogic
    private Integer isDeleted;

    // getters/setters
    public Long getArticleId() { return articleId; }
    public void setArticleId(Long articleId) { this.articleId = articleId; }
    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }
    public String getContent() { return content; }
    public void setContent(String content) { this.content = content; }
    public Long getCatId() { return catId; }
    public void setCatId(Long catId) { this.catId = catId; }
    public Integer getIsPublish() { return isPublish; }
    public void setIsPublish(Integer isPublish) { this.isPublish = isPublish; }
    public String getAuthor() { return author; }
    public void setAuthor(String author) { this.author = author; }
    public LocalDateTime getPublishTime() { return publishTime; }
    public void setPublishTime(LocalDateTime publishTime) { this.publishTime = publishTime; }
    public Integer getIsDeleted() { return isDeleted; }
    public void setIsDeleted(Integer isDeleted) { this.isDeleted = isDeleted; }
}
