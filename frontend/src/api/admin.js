import axios from 'axios'

// ============ 仪表盘 ============
export function getAdminStats() {
  return axios.get('/api/admin/stats')
}

// ============ 分类管理 ============
export function getCategoryList() {
  return axios.get('/api/admin/category/list')
}

export function addCategory(data) {
  return axios.post('/api/admin/category/add', data)
}

export function updateCategory(data) {
  return axios.put('/api/admin/category/update', data)
}

export function deleteCategory(id) {
  return axios.delete(`/api/admin/category/delete/${id}`)
}

export function toggleCategoryShow(id) {
  return axios.put(`/api/admin/category/toggle/${id}`)
}

// ============ 订单管理 ============
export function getOrderList(params) {
  return axios.get('/api/admin/order/list', { params })
}

export function getOrderDetail(orderId) {
  return axios.get(`/api/admin/order/detail/${orderId}`)
}

export function shipOrder(orderId) {
  return axios.put(`/api/admin/order/ship/${orderId}`)
}

export function refundOrder(orderId) {
  return axios.put(`/api/admin/order/refund/${orderId}`)
}

// ============ 会员管理 ============
export function getUserList(params) {
  return axios.get('/api/admin/user/list', { params })
}

export function getUserDetail(userId) {
  return axios.get(`/api/admin/user/detail/${userId}`)
}

export function toggleUserStatus(userId) {
  return axios.put(`/api/admin/user/toggle/${userId}`)
}
