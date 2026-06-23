package com.yunshop.service;

import com.yunshop.dto.OrderSubmitDto;
import com.yunshop.entity.Order;
import com.yunshop.entity.OrderGoods;
import java.util.List;

public interface OrderService {

    /** 提交订单 */
    Order submit(Long userId, OrderSubmitDto dto);

    /** 用户订单列表 */
    List<Order> findUserOrders(Long userId, String status);

    /** 订单详情 */
    Order findById(Long orderId);

    /** 订单商品 */
    List<OrderGoods> findOrderGoods(Long orderId);

    /** 取消订单 */
    void cancel(Long userId, Long orderId);

    /** 确认收货 */
    void confirmReceive(Long userId, Long orderId);

    /** 模拟支付 */
    void pay(Long userId, Long orderId);

    /** 订单状态流转（后台用） */
    void updateStatus(Long orderId, String newStatus);
}
