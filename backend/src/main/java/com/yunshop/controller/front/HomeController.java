package com.yunshop.controller.front;

import com.yunshop.common.Result;
import com.yunshop.entity.*;
import com.yunshop.service.AdService;
import com.yunshop.service.GoodsCategoryService;
import com.yunshop.service.GoodsService;
import com.yunshop.service.NavigationService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.*;

/**
 * 前台首页控制器
 */
@RestController
@RequestMapping("/api")
public class HomeController {

    @Autowired
    private NavigationService navigationService;

    @Autowired
    private GoodsCategoryService categoryService;

    @Autowired
    private GoodsService goodsService;

    @Autowired
    private AdService adService;

    /** 首页数据（导航 + 分类 + Banner + 楼层） */
    @GetMapping("/home")
    public Result<Map<String, Object>> home() {
        Map<String, Object> data = new LinkedHashMap<>();

        // 导航（前8条）
        data.put("navList", navigationService.findFrontNav(8));

        // 一级分类（前6个）+ 二级 + 三级
        List<GoodsCategory> firstLevel = categoryService.findFirstLevel(6);
        List<Map<String, Object>> categoryMenu = new ArrayList<>();
        for (GoodsCategory cat : firstLevel) {
            Map<String, Object> item = new LinkedHashMap<>();
            item.put("category", cat);
            // 二级分类及三级
            List<GoodsCategory> secondLevel = categoryService.findByParentId(cat.getId());
            List<Map<String, Object>> secondWithThird = new ArrayList<>();
            for (GoodsCategory sec : secondLevel) {
                Map<String, Object> secItem = new LinkedHashMap<>();
                secItem.put("category", sec);
                secItem.put("children", categoryService.findByParentId(sec.getId()));
                secondWithThird.add(secItem);
            }
            item.put("children", secondWithThird);
            categoryMenu.add(item);
        }
        data.put("categoryMenu", categoryMenu);

        // Banner 广告
        data.put("bannerList", adService.findEnabledBanners(5));

        // 热门楼层
        List<GoodsCategory> hotFloors = categoryService.findHotFloors();
        List<Map<String, Object>> floors = new ArrayList<>();
        for (GoodsCategory floor : hotFloors) {
            Map<String, Object> f = new LinkedHashMap<>();
            f.put("category", floor);
            f.put("subCategories", categoryService.findByParentId(floor.getId()));
            f.put("goodsList", goodsService.findByCategory(floor.getId(), 6));
            floors.add(f);
        }
        data.put("floors", floors);

        // 热门推荐
        data.put("hotGoods", goodsService.findHotRecommend(4));

        return Result.ok(data);
    }

    /** 分类菜单（含二三级） */
    @GetMapping("/categories/menu")
    public Result<List<Map<String, Object>>> categoryMenu() {
        List<GoodsCategory> firstLevel = categoryService.findFirstLevel(6);
        List<Map<String, Object>> menu = new ArrayList<>();
        for (GoodsCategory cat : firstLevel) {
            Map<String, Object> item = new LinkedHashMap<>();
            item.put("category", cat);
            // 二级分类及三级
            List<GoodsCategory> secondLevel = categoryService.findByParentId(cat.getId());
            List<Map<String, Object>> secondWithThird = new ArrayList<>();
            for (GoodsCategory sec : secondLevel) {
                Map<String, Object> secItem = new LinkedHashMap<>();
                secItem.put("category", sec);
                secItem.put("children", categoryService.findByParentId(sec.getId()));
                secondWithThird.add(secItem);
            }
            item.put("children", secondWithThird);
            menu.add(item);
        }
        return Result.ok(menu);
    }
}
