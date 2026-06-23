package com.yunshop.entity;

import com.baomidou.mybatisplus.annotation.*;
import java.math.BigDecimal;
import java.time.LocalDateTime;

/**
 * 订单实体 (order 表)
 */
@TableName("`order`")
public class Order {

    @TableId(type = IdType.AUTO)
    private Long orderId;

    private String orderSn;

    private Long userId;

    private String orderStatus;

    private Integer payStatus;

    private Integer shippingStatus;

    private BigDecimal orderAmount;

    private BigDecimal totalAmount;

    private BigDecimal shippingFee;

    private String payName;

    private String shippingName;

    private LocalDateTime payTime;

    private LocalDateTime shippingTime;

    private LocalDateTime receiveTime;

    private LocalDateTime addTime;

    private String addressSnapshot;

    private String remark;

    @TableLogic
    private Integer isDeleted;

    // getters/setters
    public Long getOrderId() { return orderId; }
    public void setOrderId(Long orderId) { this.orderId = orderId; }
    public String getOrderSn() { return orderSn; }
    public void setOrderSn(String orderSn) { this.orderSn = orderSn; }
    public Long getUserId() { return userId; }
    public void setUserId(Long userId) { this.userId = userId; }
    public String getOrderStatus() { return orderStatus; }
    public void setOrderStatus(String orderStatus) { this.orderStatus = orderStatus; }
    public Integer getPayStatus() { return payStatus; }
    public void setPayStatus(Integer payStatus) { this.payStatus = payStatus; }
    public Integer getShippingStatus() { return shippingStatus; }
    public void setShippingStatus(Integer shippingStatus) { this.shippingStatus = shippingStatus; }
    public BigDecimal getOrderAmount() { return orderAmount; }
    public void setOrderAmount(BigDecimal orderAmount) { this.orderAmount = orderAmount; }
    public BigDecimal getTotalAmount() { return totalAmount; }
    public void setTotalAmount(BigDecimal totalAmount) { this.totalAmount = totalAmount; }
    public BigDecimal getShippingFee() { return shippingFee; }
    public void setShippingFee(BigDecimal shippingFee) { this.shippingFee = shippingFee; }
    public String getPayName() { return payName; }
    public void setPayName(String payName) { this.payName = payName; }
    public String getShippingName() { return shippingName; }
    public void setShippingName(String shippingName) { this.shippingName = shippingName; }
    public LocalDateTime getPayTime() { return payTime; }
    public void setPayTime(LocalDateTime payTime) { this.payTime = payTime; }
    public LocalDateTime getShippingTime() { return shippingTime; }
    public void setShippingTime(LocalDateTime shippingTime) { this.shippingTime = shippingTime; }
    public LocalDateTime getReceiveTime() { return receiveTime; }
    public void setReceiveTime(LocalDateTime receiveTime) { this.receiveTime = receiveTime; }
    public LocalDateTime getAddTime() { return addTime; }
    public void setAddTime(LocalDateTime addTime) { this.addTime = addTime; }
    public String getAddressSnapshot() { return addressSnapshot; }
    public void setAddressSnapshot(String addressSnapshot) { this.addressSnapshot = addressSnapshot; }
    public String getRemark() { return remark; }
    public void setRemark(String remark) { this.remark = remark; }
    public Integer getIsDeleted() { return isDeleted; }
    public void setIsDeleted(Integer isDeleted) { this.isDeleted = isDeleted; }
}
