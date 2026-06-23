import request from './index'

export const submitOrder = (data) => request.post('/order/submit', data)
export const getOrderList = (status) => request.get('/order/list', { params: { status } })
export const getOrderDetail = (orderId) => request.get(`/order/detail/${orderId}`)
export const cancelOrder = (orderId) => request.put(`/order/cancel/${orderId}`)
export const payOrder = (orderId) => request.put(`/order/pay/${orderId}`)
export const confirmReceive = (orderId) => request.put(`/order/receive/${orderId}`)
