package com.yunshop.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.yunshop.entity.GoodsCategory;
import com.yunshop.mapper.GoodsCategoryMapper;
import com.yunshop.service.GoodsCategoryService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class GoodsCategoryServiceImpl implements GoodsCategoryService {

    @Autowired
    private GoodsCategoryMapper categoryMapper;

    @Override
    public List<GoodsCategory> findFirstLevel(int limit) {
        return categoryMapper.selectList(new LambdaQueryWrapper<GoodsCategory>()
                .eq(GoodsCategory::getLevel, 1)
                .eq(GoodsCategory::getIsShow, 1)
                .orderByAsc(GoodsCategory::getSortOrder)
                .last("LIMIT " + limit));
    }

    @Override
    public List<GoodsCategory> findByParentId(Long parentId) {
        return categoryMapper.selectList(new LambdaQueryWrapper<GoodsCategory>()
                .eq(GoodsCategory::getParentId, parentId)
                .eq(GoodsCategory::getIsShow, 1)
                .orderByAsc(GoodsCategory::getSortOrder));
    }

    @Override
    public List<GoodsCategory> findHotFloors() {
        return categoryMapper.selectList(new LambdaQueryWrapper<GoodsCategory>()
                .eq(GoodsCategory::getLevel, 1)
                .eq(GoodsCategory::getIsShow, 1)
                .eq(GoodsCategory::getIsHot, 1)
                .orderByAsc(GoodsCategory::getSortOrder));
    }

    @Override
    public GoodsCategory findById(Long id) {
        return categoryMapper.selectById(id);
    }

    @Override
    public List<Long> getCategoryAndChildrenIds(Long catId) {
        List<Long> ids = new ArrayList<>();
        ids.add(catId);
        // 递归查找子分类
        List<GoodsCategory> children = findByParentId(catId);
        for (GoodsCategory child : children) {
            ids.addAll(getCategoryAndChildrenIds(child.getId()));
        }
        return ids;
    }
}
