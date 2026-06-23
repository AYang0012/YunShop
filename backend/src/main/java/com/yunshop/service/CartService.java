package com.yunshop.service;

import com.yunshop.dto.CartItemDto;
import com.yunshop.entity.Cart;
import java.util.List;

public interface CartService {

    /** 加入购物车 */
    void add(Long userId, Long goodsId, Integer goodsNum, Long goodsAttrId);

    /** 购物车列表 */
    List<CartItemDto> list(Long userId);

    /** 修改数量 */
    void updateNum(Long userId, Long cartId, Integer num);

    /** 删除 */
    void delete(Long userId, Long cartId);

    /** 批量删除 */
    void deleteBatch(Long userId, List<Long> cartIds);

    /** 选中/取消 */
    void toggleSelect(Long userId, Long cartId);

    /** 全选/取消全选 */
    void selectAll(Long userId, boolean selected);

    /** 购物车商品种类数 */
    int countByUser(Long userId);
}
