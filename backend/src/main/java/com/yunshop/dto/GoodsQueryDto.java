package com.yunshop.dto;

/**
 * 商品查询条件 DTO
 */
public class GoodsQueryDto {

    private Long catId;           // 分类ID
    private String keyword;       // 搜索关键词
    private String sort;          // 排序字段(price/sales/time)
    private String order;         // 排序方向(asc/desc)
    private Integer page = 1;     // 当前页
    private Integer pageSize = 12; // 每页条数

    public Long getCatId() { return catId; }
    public void setCatId(Long catId) { this.catId = catId; }
    public String getKeyword() { return keyword; }
    public void setKeyword(String keyword) { this.keyword = keyword; }
    public String getSort() { return sort; }
    public void setSort(String sort) { this.sort = sort; }
    public String getOrder() { return order; }
    public void setOrder(String order) { this.order = order; }
    public Integer getPage() { return page; }
    public void setPage(Integer page) { this.page = page; }
    public Integer getPageSize() { return pageSize; }
    public void setPageSize(Integer pageSize) { this.pageSize = pageSize; }
}
