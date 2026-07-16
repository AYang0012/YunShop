package com.yunshop.controller.admin;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.yunshop.common.Constants;
import com.yunshop.common.PageResult;
import com.yunshop.common.Result;
import com.yunshop.entity.Admin;
import com.yunshop.entity.Order;
import com.yunshop.entity.OrderGoods;
import com.yunshop.entity.User;
import com.yunshop.mapper.OrderGoodsMapper;
import com.yunshop.mapper.OrderMapper;
import com.yunshop.mapper.UserMapper;
import com.yunshop.service.OrderService;
import jakarta.servlet.http.HttpSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * 后台订单管理控制器
 */
@RestController
@RequestMapping("/api/admin/order")
public class AdminOrderController {

    @Autowired
    private OrderMapper orderMapper;

    @Autowired
    private OrderGoodsMapper orderGoodsMapper;

    @Autowired
    private UserMapper userMapper;

    @Autowired
    private OrderService orderService;

    /** 验证管理员登录 */
    private void checkAdmin(HttpSession session) {
        Admin admin = (Admin) session.getAttribute(Constants.SESSION_ADMIN);
        if (admin == null) throw new RuntimeException("请先登录后台");
    }

    /** 订单列表（分页+筛选） */
    @GetMapping("/list")
    public Result<?> list(
            @RequestParam(defaultValue = "1") int page,
            @RequestParam(defaultValue = "20") int pageSize,
            @RequestParam(required = false) String orderSn,
            @RequestParam(required = false) String status,
            @RequestParam(required = false) Long userId,
            HttpSession session) {
        try {
            checkAdmin(session);

            LambdaQueryWrapper<Order> wrapper = new LambdaQueryWrapper<>();
            if (orderSn != null && !orderSn.isEmpty()) {
                wrapper.like(Order::getOrderSn, orderSn);
            }
            if (status != null && !status.isEmpty()) {
                wrapper.eq(Order::getOrderStatus, status);
            }
            if (userId != null) {
                wrapper.eq(Order::getUserId, userId);
            }
            wrapper.orderByDesc(Order::getAddTime);

            Page<Order> pageObj = new Page<>(page, pageSize);
            Page<Order> result = orderMapper.selectPage(pageObj, wrapper);

            // 补充用户信息
            List<Map<String, Object>> list = result.getRecords().stream().map(order -> {
                Map<String, Object> item = new HashMap<>();
                item.put("orderId", order.getOrderId());
                item.put("orderSn", order.getOrderSn());
                item.put("userId", order.getUserId());
                item.put("orderStatus", order.getOrderStatus());
                item.put("payStatus", order.getPayStatus());
                item.put("shippingStatus", order.getShippingStatus());
                item.put("totalAmount", order.getTotalAmount());
                item.put("orderAmount", order.getOrderAmount());
                item.put("shippingFee", order.getShippingFee());
                item.put("payName", order.getPayName());
                item.put("addTime", order.getAddTime());
                item.put("remark", order.getRemark());

                // 查询用户名
                User user = userMapper.selectById(order.getUserId());
                if (user != null) {
                    item.put("userNickname", user.getNickname());
                    item.put("userMobile", user.getMobile());
                }
                return item;
            }).toList();

            return Result.ok(PageResult.of(result.getTotal(), page, pageSize, list));
        } catch (RuntimeException e) {
            return Result.fail(e.getMessage());
        }
    }

    /** 订单详情 */
    @GetMapping("/detail/{orderId}")
    public Result<?> detail(@PathVariable Long orderId, HttpSession session) {
        try {
            checkAdmin(session);

            Order order = orderMapper.selectById(orderId);
            if (order == null) return Result.fail("订单不存在");

            // 查询订单商品
            List<OrderGoods> goodsList = orderGoodsMapper.selectList(
                    new LambdaQueryWrapper<OrderGoods>().eq(OrderGoods::getOrderId, orderId));

            // 查询用户信息
            User user = userMapper.selectById(order.getUserId());

            Map<String, Object> data = new HashMap<>();
            data.put("order", order);
            data.put("goodsList", goodsList);
            if (user != null) {
                Map<String, Object> userInfo = new HashMap<>();
                userInfo.put("userId", user.getUserId());
                userInfo.put("nickname", user.getNickname());
                userInfo.put("mobile", user.getMobile());
                userInfo.put("email", user.getEmail());
                data.put("user", userInfo);
            }

            return Result.ok(data);
        } catch (RuntimeException e) {
            return Result.fail(e.getMessage());
        }
    }

    /** 发货 */
    @PutMapping("/ship/{orderId}")
    public Result<?> ship(@PathVariable Long orderId, HttpSession session) {
        try {
            checkAdmin(session);
            orderService.updateStatus(orderId, Constants.ORDER_SHIPPED);
            return Result.ok("发货成功");
        } catch (RuntimeException e) {
            return Result.fail(e.getMessage());
        }
    }

    /** 退款 */
    @PutMapping("/refund/{orderId}")
    public Result<?> refund(@PathVariable Long orderId, HttpSession session) {
        try {
            checkAdmin(session);
            orderService.updateStatus(orderId, Constants.ORDER_REFUNDED);
            return Result.ok("退款成功");
        } catch (RuntimeException e) {
            return Result.fail(e.getMessage());
        }
    }
}
