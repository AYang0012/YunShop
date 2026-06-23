package com.yunshop.dto;

/**
 * 订单提交 DTO
 */
public class OrderSubmitDto {

    private Long addressId;         // 收货地址ID
    private String payName;         // 支付方式
    private String shippingName;    // 配送方式
    private String remark;          // 订单备注
    private String cartIds;         // 结算的购物车ID（逗号分隔）

    public Long getAddressId() { return addressId; }
    public void setAddressId(Long addressId) { this.addressId = addressId; }
    public String getPayName() { return payName; }
    public void setPayName(String payName) { this.payName = payName; }
    public String getShippingName() { return shippingName; }
    public void setShippingName(String shippingName) { this.shippingName = shippingName; }
    public String getRemark() { return remark; }
    public void setRemark(String remark) { this.remark = remark; }
    public String getCartIds() { return cartIds; }
    public void setCartIds(String cartIds) { this.cartIds = cartIds; }
}
