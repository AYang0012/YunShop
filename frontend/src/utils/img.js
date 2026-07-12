/**
 * 图片 URL 处理工具
 * 开发环境：Vite 代理自动转发 /upload 和 /api 到后端
 * 生产环境：需要拼接后端域名
 */
const IMG_BASE = import.meta.env.VITE_IMG_BASE || ''

/**
 * 将相对图片路径转为完整 URL
 * @param {string} path - 相对路径，如 /upload/goods/1.jpg
 * @returns {string} 完整 URL
 */
export function imgUrl(path) {
  if (!path) return ''
  if (path.startsWith('http')) return path
  return IMG_BASE + path
}
