package com.yunshop.controller.admin;

import com.yunshop.common.Constants;
import com.yunshop.common.Result;
import com.yunshop.entity.Admin;
import com.yunshop.mapper.GoodsMapper;
import com.yunshop.mapper.OrderMapper;
import com.yunshop.mapper.UserMapper;
import jakarta.servlet.http.HttpSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

/**
 * 后台仪表盘统计控制器
 */
@RestController
@RequestMapping("/api/admin")
public class AdminDashboardController {

    @Autowired
    private GoodsMapper goodsMapper;

    @Autowired
    private OrderMapper orderMapper;

    @Autowired
    private UserMapper userMapper;

    /** 获取仪表盘统计数据 */
    @GetMapping("/stats")
    public Result<?> stats(HttpSession session) {
        Admin admin = (Admin) session.getAttribute(Constants.SESSION_ADMIN);
        if (admin == null) return Result.fail(401, "请先登录后台");

        Map<String, Object> data = new HashMap<>();
        data.put("goodsCount", goodsMapper.selectCount(null));
        data.put("orderCount", orderMapper.selectCount(null));
        data.put("userCount", userMapper.selectCount(null));

        // 计算总销售额（已付款+已发货+已完成的订单）
        // 简化处理：直接查询所有非取消订单的总额
        Double totalSales = orderMapper.selectObjs(
                new com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper<com.yunshop.entity.Order>()
                        .ne(com.yunshop.entity.Order::getOrderStatus, Constants.ORDER_CANCELLED)
                        .select(com.yunshop.entity.Order::getTotalAmount)
        ).stream()
                .filter(obj -> obj != null)
                .mapToDouble(obj -> ((java.math.BigDecimal) obj).doubleValue())
                .sum();
        data.put("totalSales", String.format("%.2f", totalSales));

        return Result.ok(data);
    }
}
