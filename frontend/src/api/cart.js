import request from './index'

export const getCartList = () => request.get('/cart/list')
export const addToCart = (goodsId, num = 1, attrId = 0) =>
  request.post('/cart/add', { goodsId, num, attrId })
export const updateCartNum = (cartId, num) =>
  request.put(`/cart/update/${cartId}`, { num })
export const deleteCartItem = (cartId) =>
  request.delete(`/cart/delete/${cartId}`)
export const deleteCartBatch = (ids) =>
  request.post('/cart/delete-batch', { ids })
export const toggleCartItem = (cartId) =>
  request.put(`/cart/toggle/${cartId}`)
export const selectAll = (selected) =>
  request.put('/cart/select-all', { selected })
export const getCartCount = () => request.get('/cart/count')
