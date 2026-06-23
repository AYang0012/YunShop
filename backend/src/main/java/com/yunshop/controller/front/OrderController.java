package com.yunshop.controller.front;

import com.yunshop.common.Constants;
import com.yunshop.common.Result;
import com.yunshop.dto.OrderSubmitDto;
import com.yunshop.entity.Order;
import com.yunshop.entity.OrderGoods;
import com.yunshop.entity.User;
import com.yunshop.service.OrderService;
import jakarta.servlet.http.HttpSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

/**
 * 前台订单控制器
 */
@RestController
@RequestMapping("/api/order")
public class OrderController {

    @Autowired
    private OrderService orderService;

    private Long getUserId(HttpSession session) {
        User user = (User) session.getAttribute(Constants.SESSION_USER);
        if (user == null) throw new RuntimeException("请先登录");
        return user.getUserId();
    }

    /** 提交订单 */
    @PostMapping("/submit")
    public Result<Order> submit(@RequestBody OrderSubmitDto dto, HttpSession session) {
        try {
            Order order = orderService.submit(getUserId(session), dto);
            return Result.ok("下单成功", order);
        } catch (RuntimeException e) {
            return Result.fail(e.getMessage());
        }
    }

    /** 订单列表 */
    @GetMapping("/list")
    public Result<List<Order>> list(@RequestParam(required = false) String status, HttpSession session) {
        try {
            return Result.ok(orderService.findUserOrders(getUserId(session), status));
        } catch (RuntimeException e) {
            return Result.fail(e.getMessage());
        }
    }

    /** 订单详情 */
    @GetMapping("/detail/{orderId}")
    public Result<Map<String, Object>> detail(@PathVariable Long orderId, HttpSession session) {
        try {
            Long userId = getUserId(session);
            Order order = orderService.findById(orderId);
            if (order == null || !order.getUserId().equals(userId)) {
                return Result.fail("订单不存在");
            }
            List<OrderGoods> goods = orderService.findOrderGoods(orderId);
            Map<String, Object> data = new java.util.LinkedHashMap<>();
            data.put("order", order);
            data.put("goodsList", goods);
            return Result.ok(data);
        } catch (RuntimeException e) {
            return Result.fail(e.getMessage());
        }
    }

    /** 取消订单 */
    @PutMapping("/cancel/{orderId}")
    public Result<?> cancel(@PathVariable Long orderId, HttpSession session) {
        try {
            orderService.cancel(getUserId(session), orderId);
            return Result.ok("订单已取消");
        } catch (RuntimeException e) {
            return Result.fail(e.getMessage());
        }
    }

    /** 模拟支付 */
    @PutMapping("/pay/{orderId}")
    public Result<?> pay(@PathVariable Long orderId, HttpSession session) {
        try {
            orderService.pay(getUserId(session), orderId);
            return Result.ok("支付成功");
        } catch (RuntimeException e) {
            return Result.fail(e.getMessage());
        }
    }

    /** 确认收货 */
    @PutMapping("/receive/{orderId}")
    public Result<?> confirmReceive(@PathVariable Long orderId, HttpSession session) {
        try {
            orderService.confirmReceive(getUserId(session), orderId);
            return Result.ok("已确认收货");
        } catch (RuntimeException e) {
            return Result.fail(e.getMessage());
        }
    }
}
