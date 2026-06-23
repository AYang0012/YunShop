package com.yunshop.controller.front;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.yunshop.common.PageResult;
import com.yunshop.common.Result;
import com.yunshop.dto.GoodsQueryDto;
import com.yunshop.entity.Goods;
import com.yunshop.entity.GoodsAttr;
import com.yunshop.entity.GoodsImage;
import com.yunshop.mapper.GoodsAttrMapper;
import com.yunshop.service.GoodsService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * 前台商品控制器
 */
@RestController
@RequestMapping("/api/goods")
public class GoodsController {

    @Autowired
    private GoodsService goodsService;

    @Autowired
    private GoodsAttrMapper goodsAttrMapper;

    /** 商品列表（分页 + 筛选 + 排序 + 搜索） */
    @GetMapping("/list")
    public Result<PageResult<Goods>> list(GoodsQueryDto query) {
        Page<Goods> page = goodsService.findPage(query);
        PageResult<Goods> result = PageResult.of(
                page.getTotal(),
                (int) page.getCurrent(),
                (int) page.getSize(),
                page.getRecords()
        );
        return Result.ok(result);
    }

    /** 商品详情 */
    @GetMapping("/detail/{goodsId}")
    public Result<java.util.Map<String, Object>> detail(@PathVariable Long goodsId) {
        Goods goods = goodsService.findById(goodsId);
        if (goods == null || goods.getIsOnSale() == 0) {
            return Result.fail("商品不存在或已下架");
        }

        List<GoodsImage> images = goodsService.findImages(goodsId);
        List<GoodsAttr> attrs = goodsAttrMapper.selectList(
                new com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper<GoodsAttr>()
                        .eq(GoodsAttr::getGoodsId, goodsId));

        java.util.Map<String, Object> data = new java.util.LinkedHashMap<>();
        data.put("goods", goods);
        data.put("images", images);
        data.put("attrs", attrs);
        return Result.ok(data);
    }

    /** 热门推荐 */
    @GetMapping("/hot")
    public Result<List<Goods>> hot(@RequestParam(defaultValue = "8") int limit) {
        return Result.ok(goodsService.findHotRecommend(limit));
    }

    /** 关键词搜索 */
    @GetMapping("/search")
    public Result<PageResult<Goods>> search(
            @RequestParam String keyword,
            @RequestParam(defaultValue = "1") int page,
            @RequestParam(defaultValue = "12") int pageSize) {
        GoodsQueryDto query = new GoodsQueryDto();
        query.setKeyword(keyword);
        query.setPage(page);
        query.setPageSize(pageSize);
        Page<Goods> result = goodsService.findPage(query);
        return Result.ok(PageResult.of(result.getTotal(), page, pageSize, result.getRecords()));
    }
}
