package com.yunshop.controller.front;

import com.yunshop.common.Constants;
import com.yunshop.common.Result;
import com.yunshop.dto.CartItemDto;
import com.yunshop.entity.User;
import com.yunshop.service.CartService;
import jakarta.servlet.http.HttpSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

/**
 * 前台购物车控制器
 */
@RestController
@RequestMapping("/api/cart")
public class CartController {

    @Autowired
    private CartService cartService;

    private Long getUserId(HttpSession session) {
        User user = (User) session.getAttribute(Constants.SESSION_USER);
        if (user == null) throw new RuntimeException("请先登录");
        return user.getUserId();
    }

    /** 购物车列表 */
    @GetMapping("/list")
    public Result<List<CartItemDto>> list(HttpSession session) {
        try {
            return Result.ok(cartService.list(getUserId(session)));
        } catch (RuntimeException e) {
            return Result.fail(e.getMessage());
        }
    }

    /** 加入购物车 */
    @PostMapping("/add")
    public Result<?> add(@RequestBody Map<String, Object> params, HttpSession session) {
        try {
            Long userId = getUserId(session);
            Long goodsId = Long.valueOf(params.get("goodsId").toString());
            Integer num = params.containsKey("num") ? Integer.valueOf(params.get("num").toString()) : 1;
            Long attrId = params.containsKey("attrId") ? Long.valueOf(params.get("attrId").toString()) : 0L;
            cartService.add(userId, goodsId, num, attrId);
            return Result.ok("已加入购物车");
        } catch (RuntimeException e) {
            return Result.fail(e.getMessage());
        }
    }

    /** 修改数量 */
    @PutMapping("/update/{cartId}")
    public Result<?> updateNum(@PathVariable Long cartId, @RequestBody Map<String, Integer> params, HttpSession session) {
        try {
            cartService.updateNum(getUserId(session), cartId, params.get("num"));
            return Result.ok();
        } catch (RuntimeException e) {
            return Result.fail(e.getMessage());
        }
    }

    /** 删除 */
    @DeleteMapping("/delete/{cartId}")
    public Result<?> delete(@PathVariable Long cartId, HttpSession session) {
        try {
            cartService.delete(getUserId(session), cartId);
            return Result.ok();
        } catch (RuntimeException e) {
            return Result.fail(e.getMessage());
        }
    }

    /** 批量删除 */
    @PostMapping("/delete-batch")
    public Result<?> deleteBatch(@RequestBody Map<String, List<Long>> params, HttpSession session) {
        try {
            cartService.deleteBatch(getUserId(session), params.get("ids"));
            return Result.ok();
        } catch (RuntimeException e) {
            return Result.fail(e.getMessage());
        }
    }

    /** 切换选中 */
    @PutMapping("/toggle/{cartId}")
    public Result<?> toggleSelect(@PathVariable Long cartId, HttpSession session) {
        try {
            cartService.toggleSelect(getUserId(session), cartId);
            return Result.ok();
        } catch (RuntimeException e) {
            return Result.fail(e.getMessage());
        }
    }

    /** 全选/取消全选 */
    @PutMapping("/select-all")
    public Result<?> selectAll(@RequestBody Map<String, Boolean> params, HttpSession session) {
        try {
            cartService.selectAll(getUserId(session), params.get("selected"));
            return Result.ok();
        } catch (RuntimeException e) {
            return Result.fail(e.getMessage());
        }
    }

    /** 购物车数量 */
    @GetMapping("/count")
    public Result<Integer> count(HttpSession session) {
        User user = (User) session.getAttribute(Constants.SESSION_USER);
        if (user == null) return Result.ok(0);
        return Result.ok(cartService.countByUser(user.getUserId()));
    }
}
