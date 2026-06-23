import request from './index'

export const getCaptcha = () => request.get('/user/captcha')
export const login = (data) => request.post('/user/login', data)
export const register = (data) => request.post('/user/register', data)
export const logout = () => request.post('/user/logout')
export const getCurrentUser = () => request.get('/user/current')
export const checkLogin = () => request.get('/user/check')
export const updateProfile = (data) => request.put('/user/profile', data)
export const changePassword = (data) => request.put('/user/password', data)
export const uploadAvatar = (file) => {
  const formData = new FormData()
  formData.append('file', file)
  return request.post('/upload/avatar', formData)
}
