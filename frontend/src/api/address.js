import request from './index'

export const getAddressList = () => request.get('/address/list')
export const getAddress = (id) => request.get(`/address/${id}`)
export const addAddress = (data) => request.post('/address/add', data)
export const updateAddress = (data) => request.put('/address/update', data)
export const deleteAddress = (id) => request.delete(`/address/delete/${id}`)
export const setDefaultAddress = (id) => request.put(`/address/default/${id}`)
