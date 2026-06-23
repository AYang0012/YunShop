package com.yunshop.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.yunshop.common.Constants;
import com.yunshop.dto.CartItemDto;
import com.yunshop.dto.OrderSubmitDto;
import com.yunshop.entity.*;
import com.yunshop.mapper.*;
import com.yunshop.service.CartService;
import com.yunshop.service.OrderService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.Random;

@Service
public class OrderServiceImpl implements OrderService {

    @Autowired
    private OrderMapper orderMapper;

    @Autowired
    private OrderGoodsMapper orderGoodsMapper;

    @Autowired
    private CartService cartService;

    @Autowired
    private CartMapper cartMapper;

    @Autowired
    private GoodsMapper goodsMapper;

    @Autowired
    private AddressMapper addressMapper;

    @Override
    @Transactional
    public Order submit(Long userId, OrderSubmitDto dto) {
        // 获取收货地址
        Address address = addressMapper.selectById(dto.getAddressId());
        if (address == null || !address.getUserId().equals(userId)) {
            throw new RuntimeException("收货地址不存在");
        }

        // 获取选中的购物车商品
        List<CartItemDto> cartItems = cartService.list(userId);
        List<CartItemDto> selected = cartItems.stream()
                .filter(c -> c.getSelected() == 1)
                .toList();

        if (selected.isEmpty()) {
            throw new RuntimeException("请选择要结算的商品");
        }

        // 计算金额
        BigDecimal totalAmount = BigDecimal.ZERO;
        for (CartItemDto item : selected) {
            totalAmount = totalAmount.add(item.getSubtotal());
        }

        // 创建订单
        Order order = new Order();
        order.setOrderSn(generateOrderSn());
        order.setUserId(userId);
        order.setOrderStatus(Constants.ORDER_PENDING);
        order.setPayStatus(0);
        order.setShippingStatus(0);
        order.setTotalAmount(totalAmount);
        order.setOrderAmount(totalAmount.add(order.getShippingFee() != null ? order.getShippingFee() : BigDecimal.ZERO));
        order.setShippingFee(BigDecimal.ZERO); // 暂免运费
        order.setPayName(dto.getPayName());
        order.setShippingName(dto.getShippingName());
        order.setRemark(dto.getRemark());
        order.setAddTime(LocalDateTime.now());

        // 地址快照
        String addrSnapshot = String.format("{\"consignee\":\"%s\",\"mobile\":\"%s\",\"address\":\"%s%s%s%s\"}",
                address.getConsignee(), address.getMobile(),
                address.getProvince(), address.getCity(), address.getDistrict(), address.getAddress());
        order.setAddressSnapshot(addrSnapshot);

        orderMapper.insert(order);

        // 创建订单商品记录
        for (CartItemDto item : selected) {
            OrderGoods og = new OrderGoods();
            og.setOrderId(order.getOrderId());
            og.setGoodsId(item.getGoodsId());
            og.setGoodsName(item.getGoodsName());
            og.setGoodsPrice(item.getGoodsPrice());
            og.setGoodsNum(item.getGoodsNum());
            og.setGoodsImage(item.getGoodsThumb());
            og.setGoodsAttr(item.getAttrInfo());
            orderGoodsMapper.insert(og);

            // 扣减库存 + 增加销量
            Goods goods = goodsMapper.selectById(item.getGoodsId());
            if (goods != null) {
                goods.setStoreCount(goods.getStoreCount() - item.getGoodsNum());
                goods.setSalesSum(goods.getSalesSum() + item.getGoodsNum());
                goodsMapper.updateById(goods);
            }
        }

        // 清除已结算的购物车记录
        List<Long> cartIds = cartMapper.selectList(new LambdaQueryWrapper<Cart>()
                        .eq(Cart::getUserId, userId)
                        .eq(Cart::getSelected, 1))
                .stream().map(Cart::getId).toList();
        cartService.deleteBatch(userId, cartIds);

        return order;
    }

    @Override
    public List<Order> findUserOrders(Long userId, String status) {
        LambdaQueryWrapper<Order> wrapper = new LambdaQueryWrapper<Order>()
                .eq(Order::getUserId, userId)
                .orderByDesc(Order::getAddTime);
        if (status != null && !status.isEmpty()) {
            wrapper.eq(Order::getOrderStatus, status);
        }
        return orderMapper.selectList(wrapper);
    }

    @Override
    public Order findById(Long orderId) {
        return orderMapper.selectById(orderId);
    }

    @Override
    public List<OrderGoods> findOrderGoods(Long orderId) {
        return orderGoodsMapper.selectList(new LambdaQueryWrapper<OrderGoods>()
                .eq(OrderGoods::getOrderId, orderId));
    }

    @Override
    @Transactional
    public void cancel(Long userId, Long orderId) {
        Order order = orderMapper.selectById(orderId);
        if (order == null || !order.getUserId().equals(userId)) {
            throw new RuntimeException("订单不存在");
        }
        if (!Constants.ORDER_PENDING.equals(order.getOrderStatus())) {
            throw new RuntimeException("只有待付款订单才能取消");
        }
        order.setOrderStatus(Constants.ORDER_CANCELLED);
        orderMapper.updateById(order);

        // 回滚库存
        List<OrderGoods> ogs = findOrderGoods(orderId);
        for (OrderGoods og : ogs) {
            Goods goods = goodsMapper.selectById(og.getGoodsId());
            if (goods != null) {
                goods.setStoreCount(goods.getStoreCount() + og.getGoodsNum());
                goods.setSalesSum(Math.max(0, goods.getSalesSum() - og.getGoodsNum()));
                goodsMapper.updateById(goods);
            }
        }
    }

    @Override
    public void confirmReceive(Long userId, Long orderId) {
        Order order = orderMapper.selectById(orderId);
        if (order == null || !order.getUserId().equals(userId)) {
            throw new RuntimeException("订单不存在");
        }
        if (!Constants.ORDER_SHIPPED.equals(order.getOrderStatus())) {
            throw new RuntimeException("订单状态不正确");
        }
        order.setOrderStatus(Constants.ORDER_COMPLETED);
        order.setShippingStatus(2);
        order.setReceiveTime(LocalDateTime.now());
        orderMapper.updateById(order);
    }

    @Override
    public void pay(Long userId, Long orderId) {
        Order order = orderMapper.selectById(orderId);
        if (order == null || !order.getUserId().equals(userId)) {
            throw new RuntimeException("订单不存在");
        }
        if (!Constants.ORDER_PENDING.equals(order.getOrderStatus())) {
            throw new RuntimeException("订单状态不正确");
        }
        order.setOrderStatus(Constants.ORDER_PAID);
        order.setPayStatus(1);
        order.setPayTime(LocalDateTime.now());
        orderMapper.updateById(order);
    }

    @Override
    public void updateStatus(Long orderId, String newStatus) {
        Order order = orderMapper.selectById(orderId);
        if (order == null) {
            throw new RuntimeException("订单不存在");
        }
        order.setOrderStatus(newStatus);
        if (Constants.ORDER_SHIPPED.equals(newStatus)) {
            order.setShippingStatus(1);
            order.setShippingTime(LocalDateTime.now());
        }
        orderMapper.updateById(order);
    }

    private String generateOrderSn() {
        String datePrefix = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyyMMdd"));
        String timePart = String.valueOf(System.currentTimeMillis());
        timePart = timePart.substring(timePart.length() - 10);
        String random = String.format("%02d", new Random().nextInt(100));
        return datePrefix + timePart + random;
    }
}
