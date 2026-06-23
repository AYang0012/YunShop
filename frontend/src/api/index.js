import axios from 'axios'
import { ElMessage } from 'element-plus'

const request = axios.create({
  baseURL: '/api',
  timeout: 15000,
  withCredentials: true
})

// 响应拦截
request.interceptors.response.use(
  response => {
    const data = response.data
    if (data.code === 401) {
      // 未登录，跳转登录页
      if (window.location.pathname !== '/login' && window.location.pathname !== '/register') {
        window.location.href = '/login'
      }
      return Promise.reject(new Error(data.msg))
    }
    if (data.code !== 200) {
      ElMessage.error(data.msg || '请求失败')
      return Promise.reject(new Error(data.msg))
    }
    return data
  },
  error => {
    ElMessage.error('网络错误')
    return Promise.reject(error)
  }
)

export default request
