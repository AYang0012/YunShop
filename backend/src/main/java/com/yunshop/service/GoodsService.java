package com.yunshop.service;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.yunshop.dto.GoodsQueryDto;
import com.yunshop.entity.Goods;
import com.yunshop.entity.GoodsImage;

import java.util.List;

/**
 * 商品服务接口
 */
public interface GoodsService {

    /** 分页查询商品列表 */
    Page<Goods> findPage(GoodsQueryDto query);

    /** 商品详情 */
    Goods findById(Long goodsId);

    /** 商品图片列表 */
    List<GoodsImage> findImages(Long goodsId);

    /** 热门推荐商品 */
    List<Goods> findHotRecommend(int limit);

    /** 按分类查询商品 */
    List<Goods> findByCategory(Long catId, int limit);
}
