package com.yunshop.service;

import com.yunshop.entity.GoodsCategory;
import java.util.List;

/**
 * 商品分类服务接口
 */
public interface GoodsCategoryService {

    /** 获取所有一级分类（最多6个） */
    List<GoodsCategory> findFirstLevel(int limit);

    /** 获取子分类 */
    List<GoodsCategory> findByParentId(Long parentId);

    /** 获取热门楼层分类 */
    List<GoodsCategory> findHotFloors();

    /** 根据ID查询 */
    GoodsCategory findById(Long id);

    /** 获取某个分类的所有子分类ID（含自身） */
    List<Long> getCategoryAndChildrenIds(Long catId);
}
