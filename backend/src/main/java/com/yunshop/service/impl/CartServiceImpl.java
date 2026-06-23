package com.yunshop.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.yunshop.common.Constants;
import com.yunshop.dto.CartItemDto;
import com.yunshop.entity.Cart;
import com.yunshop.entity.Goods;
import com.yunshop.entity.GoodsAttr;
import com.yunshop.mapper.CartMapper;
import com.yunshop.mapper.GoodsAttrMapper;
import com.yunshop.mapper.GoodsMapper;
import com.yunshop.service.CartService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

@Service
public class CartServiceImpl implements CartService {

    @Autowired
    private CartMapper cartMapper;

    @Autowired
    private GoodsMapper goodsMapper;

    @Autowired
    private GoodsAttrMapper goodsAttrMapper;

    @Override
    public void add(Long userId, Long goodsId, Integer goodsNum, Long goodsAttrId) {
        // 校验商品是否存在且上架
        Goods goods = goodsMapper.selectById(goodsId);
        if (goods == null || goods.getIsOnSale() == 0) {
            throw new RuntimeException("商品不存在或已下架");
        }
        // 校验库存
        if (goods.getStoreCount() < goodsNum) {
            throw new RuntimeException("库存不足");
        }
        // 校验购物车种类上限
        long typeCount = cartMapper.selectCount(new LambdaQueryWrapper<Cart>()
                .eq(Cart::getUserId, userId));
        if (typeCount >= Constants.CART_MAX_TYPES) {
            throw new RuntimeException("购物车商品种类已达上限(" + Constants.CART_MAX_TYPES + "种)");
        }

        // 确定价格（如果有SKU选择则使用SKU价格）
        BigDecimal price = goods.getShopPrice();
        if (goodsAttrId != null && goodsAttrId > 0) {
            GoodsAttr attr = goodsAttrMapper.selectById(goodsAttrId);
            if (attr != null && attr.getAttrPrice() != null) {
                price = price.add(attr.getAttrPrice());
            }
        }

        // 检查是否已在购物车中
        LambdaQueryWrapper<Cart> wrapper = new LambdaQueryWrapper<Cart>()
                .eq(Cart::getUserId, userId)
                .eq(Cart::getGoodsId, goodsId);
        if (goodsAttrId != null && goodsAttrId > 0) {
            wrapper.eq(Cart::getGoodsAttrId, goodsAttrId);
        } else {
            wrapper.eq(Cart::getGoodsAttrId, 0L);
        }
        Cart exist = cartMapper.selectOne(wrapper);
        if (exist != null) {
            // 已在购物车，累加数量
            int newNum = exist.getGoodsNum() + goodsNum;
            if (newNum > Constants.CART_MAX_QUANTITY) {
                newNum = Constants.CART_MAX_QUANTITY;
            }
            exist.setGoodsNum(newNum);
            exist.setGoodsPrice(price);
            cartMapper.updateById(exist);
        } else {
            // 新增到购物车
            Cart cart = new Cart();
            cart.setUserId(userId);
            cart.setGoodsId(goodsId);
            cart.setGoodsAttrId(goodsAttrId != null ? goodsAttrId : 0L);
            cart.setGoodsNum(Math.min(goodsNum, Constants.CART_MAX_QUANTITY));
            cart.setGoodsPrice(price);
            cart.setSelected(1);
            cart.setAddTime(LocalDateTime.now());
            cartMapper.insert(cart);
        }
    }

    @Override
    public List<CartItemDto> list(Long userId) {
        LambdaQueryWrapper<Cart> wrapper = new LambdaQueryWrapper<Cart>()
                .eq(Cart::getUserId, userId)
                .orderByDesc(Cart::getAddTime);
        List<Cart> carts = cartMapper.selectList(wrapper);

        List<CartItemDto> result = new ArrayList<>();
        for (Cart cart : carts) {
            Goods goods = goodsMapper.selectById(cart.getGoodsId());
            if (goods == null) continue;

            CartItemDto dto = new CartItemDto();
            dto.setCartId(cart.getId());
            dto.setGoodsId(goods.getGoodsId());
            dto.setGoodsName(goods.getGoodsName());
            dto.setGoodsThumb(goods.getGoodsThumb());
            dto.setGoodsPrice(cart.getGoodsPrice());
            dto.setGoodsNum(cart.getGoodsNum());
            dto.setSubtotal(cart.getGoodsPrice().multiply(BigDecimal.valueOf(cart.getGoodsNum())));
            dto.setSelected(cart.getSelected());
            dto.setStoreCount(goods.getStoreCount());

            // 规格信息
            if (cart.getGoodsAttrId() != null && cart.getGoodsAttrId() > 0) {
                GoodsAttr attr = goodsAttrMapper.selectById(cart.getGoodsAttrId());
                if (attr != null) {
                    dto.setAttrInfo(attr.getAttrName() + ": " + attr.getAttrValue());
                }
            }
            result.add(dto);
        }
        return result;
    }

    @Override
    public void updateNum(Long userId, Long cartId, Integer num) {
        if (num < Constants.CART_MIN_QUANTITY || num > Constants.CART_MAX_QUANTITY) {
            throw new RuntimeException("数量范围: " + Constants.CART_MIN_QUANTITY + "-" + Constants.CART_MAX_QUANTITY);
        }
        Cart cart = cartMapper.selectById(cartId);
        if (cart == null || !cart.getUserId().equals(userId)) {
            throw new RuntimeException("购物车记录不存在");
        }
        cart.setGoodsNum(num);
        cartMapper.updateById(cart);
    }

    @Override
    public void delete(Long userId, Long cartId) {
        Cart cart = cartMapper.selectById(cartId);
        if (cart == null || !cart.getUserId().equals(userId)) {
            throw new RuntimeException("购物车记录不存在");
        }
        cartMapper.deleteById(cartId);
    }

    @Override
    public void deleteBatch(Long userId, List<Long> cartIds) {
        for (Long id : cartIds) {
            Cart cart = cartMapper.selectById(id);
            if (cart != null && cart.getUserId().equals(userId)) {
                cartMapper.deleteById(id);
            }
        }
    }

    @Override
    public void toggleSelect(Long userId, Long cartId) {
        Cart cart = cartMapper.selectById(cartId);
        if (cart == null || !cart.getUserId().equals(userId)) return;
        cart.setSelected(cart.getSelected() == 1 ? 0 : 1);
        cartMapper.updateById(cart);
    }

    @Override
    public void selectAll(Long userId, boolean selected) {
        List<Cart> carts = cartMapper.selectList(new LambdaQueryWrapper<Cart>()
                .eq(Cart::getUserId, userId));
        for (Cart cart : carts) {
            cart.setSelected(selected ? 1 : 0);
            cartMapper.updateById(cart);
        }
    }

    @Override
    public int countByUser(Long userId) {
        return cartMapper.selectCount(new LambdaQueryWrapper<Cart>()
                .eq(Cart::getUserId, userId)).intValue();
    }
}
