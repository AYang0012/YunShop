package com.yunshop.controller.admin;

import com.yunshop.common.Constants;
import com.yunshop.common.Result;
import com.yunshop.entity.Admin;
import com.yunshop.entity.Goods;
import com.yunshop.mapper.GoodsMapper;
import jakarta.servlet.http.HttpSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;

/**
 * 后台商品管理控制器
 */
@RestController
@RequestMapping("/api/admin/goods")
public class AdminGoodsController {

    @Autowired
    private GoodsMapper goodsMapper;

    /** 验证管理员登录 */
    private void checkAdmin(HttpSession session) {
        Admin admin = (Admin) session.getAttribute(Constants.SESSION_ADMIN);
        if (admin == null) throw new RuntimeException("请先登录后台");
    }

    /** 添加商品 */
    @PostMapping("/add")
    public Result<?> add(@RequestBody Goods goods, HttpSession session) {
        try {
            checkAdmin(session);
            goods.setAddTime(LocalDateTime.now());
            goods.setUpdateTime(LocalDateTime.now());
            goodsMapper.insert(goods);
            return Result.ok("添加成功");
        } catch (RuntimeException e) {
            return Result.fail(e.getMessage());
        }
    }

    /** 更新商品 */
    @PutMapping("/update")
    public Result<?> update(@RequestBody Goods goods, HttpSession session) {
        try {
            checkAdmin(session);
            goods.setUpdateTime(LocalDateTime.now());
            goodsMapper.updateById(goods);
            return Result.ok("更新成功");
        } catch (RuntimeException e) {
            return Result.fail(e.getMessage());
        }
    }

    /** 删除商品（软删除） */
    @DeleteMapping("/delete/{goodsId}")
    public Result<?> delete(@PathVariable Long goodsId, HttpSession session) {
        try {
            checkAdmin(session);
            goodsMapper.deleteById(goodsId);
            return Result.ok("已删除");
        } catch (RuntimeException e) {
            return Result.fail(e.getMessage());
        }
    }

    /** 商品上下架切换 */
    @PutMapping("/toggle/{goodsId}")
    public Result<?> toggle(@PathVariable Long goodsId, HttpSession session) {
        try {
            checkAdmin(session);
            Goods goods = goodsMapper.selectById(goodsId);
            if (goods == null) return Result.fail("商品不存在");
            goods.setIsOnSale(goods.getIsOnSale() == 1 ? 0 : 1);
            goodsMapper.updateById(goods);
            return Result.ok(goods.getIsOnSale() == 1 ? "已上架" : "已下架");
        } catch (RuntimeException e) {
            return Result.fail(e.getMessage());
        }
    }
}
