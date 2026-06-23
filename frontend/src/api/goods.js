import request from './index'

export const getHomeData = () => request.get('/home')
export const getGoodsList = (params) => request.get('/goods/list', { params })
export const getGoodsDetail = (id) => request.get(`/goods/detail/${id}`)
export const getHotGoods = (limit = 8) => request.get('/goods/hot', { params: { limit } })
export const searchGoods = (keyword, page = 1, pageSize = 12) =>
  request.get('/goods/search', { params: { keyword, page, pageSize } })
export const getCategoryMenu = () => request.get('/categories/menu')
