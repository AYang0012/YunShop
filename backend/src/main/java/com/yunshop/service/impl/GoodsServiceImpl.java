package com.yunshop.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.yunshop.dto.GoodsQueryDto;
import com.yunshop.entity.Goods;
import com.yunshop.entity.GoodsImage;
import com.yunshop.mapper.GoodsImageMapper;
import com.yunshop.mapper.GoodsMapper;
import com.yunshop.service.GoodsCategoryService;
import com.yunshop.service.GoodsService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;

import java.util.List;

@Service
public class GoodsServiceImpl implements GoodsService {

    @Autowired
    private GoodsMapper goodsMapper;

    @Autowired
    private GoodsImageMapper goodsImageMapper;

    @Autowired
    private GoodsCategoryService categoryService;

    @Override
    public Page<Goods> findPage(GoodsQueryDto query) {
        LambdaQueryWrapper<Goods> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(Goods::getIsOnSale, 1);

        // 分类筛选（含子分类）
        if (query.getCatId() != null) {
            List<Long> catIds = categoryService.getCategoryAndChildrenIds(query.getCatId());
            wrapper.in(Goods::getCatId, catIds);
        }

        // 关键词搜索
        if (StringUtils.hasText(query.getKeyword())) {
            wrapper.and(w -> w
                    .like(Goods::getGoodsName, query.getKeyword())
                    .or()
                    .like(Goods::getKeywords, query.getKeyword()));
        }

        // 排序
        if (StringUtils.hasText(query.getSort())) {
            boolean isAsc = "asc".equalsIgnoreCase(query.getOrder());
            switch (query.getSort()) {
                case "price":
                    wrapper.orderBy(true, isAsc, Goods::getShopPrice);
                    break;
                case "sales":
                    wrapper.orderBy(true, isAsc, Goods::getSalesSum);
                    break;
                case "time":
                    wrapper.orderBy(true, isAsc, Goods::getAddTime);
                    break;
                default:
                    wrapper.orderByDesc(Goods::getSortOrder);
            }
        } else {
            wrapper.orderByDesc(Goods::getSortOrder);
        }

        Page<Goods> page = new Page<>(query.getPage(), query.getPageSize());
        return goodsMapper.selectPage(page, wrapper);
    }

    @Override
    public Goods findById(Long goodsId) {
        return goodsMapper.selectById(goodsId);
    }

    @Override
    public List<GoodsImage> findImages(Long goodsId) {
        return goodsImageMapper.selectList(new LambdaQueryWrapper<GoodsImage>()
                .eq(GoodsImage::getGoodsId, goodsId)
                .orderByAsc(GoodsImage::getSortOrder));
    }

    @Override
    public List<Goods> findHotRecommend(int limit) {
        return goodsMapper.selectList(new LambdaQueryWrapper<Goods>()
                .eq(Goods::getIsOnSale, 1)
                .eq(Goods::getIsRecommend, 1)
                .orderByDesc(Goods::getSortOrder)
                .last("LIMIT " + limit));
    }

    @Override
    public List<Goods> findByCategory(Long catId, int limit) {
        // 包含所有子分类
        List<Long> catIds = categoryService.getCategoryAndChildrenIds(catId);
        LambdaQueryWrapper<Goods> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(Goods::getIsOnSale, 1)
                .in(Goods::getCatId, catIds)
                .orderByDesc(Goods::getSortOrder)
                .last("LIMIT " + limit);
        return goodsMapper.selectList(wrapper);
    }
}
