<template>
  <header class="header">
    <div class="header-inner">
      <!-- Logo -->
      <router-link to="/" class="logo">云集优选</router-link>

      <!-- 导航链接 + 悬停下拉 -->
      <nav class="nav-links">
        <div
          v-for="nav in navList"
          :key="nav.id"
          class="nav-item-wrapper"
          @mouseenter="onNavEnter(nav)"
          @mouseleave="onNavLeave"
        >
          <router-link :to="nav.url" class="nav-item" :class="{ 'has-dropdown': hasDropdown(nav) }">
            {{ nav.name }}
            <el-icon v-if="hasDropdown(nav)" class="nav-arrow-icon"><ArrowDown /></el-icon>
          </router-link>
        </div>
      </nav>

      <!-- Mega dropdown 面板 -->
      <div
        v-if="dropdownVisible && activeNavDropdown"
        class="nav-dropdown-panel"
        @mouseenter="onPanelEnter"
        @mouseleave="onPanelLeave"
      >
        <div
          v-for="child in activeNavDropdown.children"
          :key="child.category.id"
          class="nav-dropdown-col"
        >
          <router-link
            :to="`/goods/list?catId=${child.category.id}`"
            class="nav-dropdown-title"
          >
            {{ child.category.name }}
          </router-link>
          <div class="nav-dropdown-tags">
            <router-link
              v-for="grandchild in child.children"
              :key="grandchild.id"
              :to="`/goods/list?catId=${grandchild.id}`"
              class="nav-dropdown-tag"
            >
              {{ grandchild.name }}
            </router-link>
          </div>
        </div>
      </div>

      <!-- 用户区 + 购物车 -->
      <div class="header-actions">
        <template v-if="user">
          <router-link to="/user" class="user-info">
            <el-avatar v-if="user.avatar" :size="32" :src="user.avatar" class="user-avatar" />
            <el-avatar v-else :size="32" class="user-avatar-default">
              {{ user.nickname ? user.nickname.charAt(0).toUpperCase() : 'U' }}
            </el-avatar>
            <span class="user-name">{{ user.nickname }}</span>
          </router-link>
          <el-button text @click="handleLogout">安全退出</el-button>
        </template>
        <template v-else>
          <router-link to="/login" class="link">登录</router-link>
          <span class="divider">|</span>
          <router-link to="/register" class="link">注册</router-link>
        </template>
        <router-link to="/cart" class="cart-link">
          <el-icon :size="22"><ShoppingCart /></el-icon>
          <span v-if="cartCount > 0" class="cart-badge">{{ cartCount }}</span>
        </router-link>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getHomeData } from '@/api/goods'
import { checkLogin, logout, getCurrentUser } from '@/api/user'
import { getCartCount } from '@/api/cart'

const navList = ref([])
const categories = ref([])
const user = ref(null)
const cartCount = ref(0)

// 下拉状态
const activeNavId = ref(null)
const dropdownVisible = ref(false)
let hideTimer = null

// 从 URL 中提取 catId
const extractCatId = (url) => {
  if (!url) return null
  const match = url.match(/catId=(\d+)/)
  return match ? parseInt(match[1]) : null
}

// 判断导航项是否有下拉（URL中有catId，且分类树中有子分类）
const hasDropdown = (nav) => {
  const catId = extractCatId(nav.url)
  if (!catId) return false
  return categories.value.some(c => c.category.id === catId && c.children && c.children.length > 0)
}

// 当前激活导航项的下拉数据
const activeNavDropdown = computed(() => {
  if (!activeNavId.value) return null
  const nav = navList.value.find(n => n.id === activeNavId.value)
  if (!nav) return null
  const catId = extractCatId(nav.url)
  if (!catId) return null
  return categories.value.find(c => c.category.id === catId) || null
})

// 悬停交互
const clearHideTimer = () => {
  if (hideTimer) {
    clearTimeout(hideTimer)
    hideTimer = null
  }
}

const onNavEnter = (nav) => {
  clearHideTimer()
  if (hasDropdown(nav)) {
    activeNavId.value = nav.id
    dropdownVisible.value = true
  } else {
    // 无下拉的导航项，关闭当前下拉
    activeNavId.value = null
    dropdownVisible.value = false
  }
}

const onNavLeave = () => {
  hideTimer = setTimeout(() => {
    activeNavId.value = null
    dropdownVisible.value = false
  }, 150)
}

const onPanelEnter = () => {
  clearHideTimer()
}

const onPanelLeave = () => {
  activeNavId.value = null
  dropdownVisible.value = false
}

// 退出登录
const handleLogout = async () => {
  await logout()
  user.value = null
  cartCount.value = 0
}

// 加载数据
onMounted(async () => {
  try {
    const res = await getHomeData()
    if (res.code === 200) {
      const d = res.data
      navList.value = d.navList || []
      categories.value = d.categoryMenu || []
    }
  } catch (e) { /* 使用默认空值 */ }
  try {
    const checkRes = await checkLogin()
    if (checkRes.data) {
      const curRes = await getCurrentUser()
      if (curRes.code === 200) user.value = curRes.data
    }
  } catch (e) { /* 未登录 */ }
  try {
    const c = await getCartCount()
    if (c.code === 200) cartCount.value = c.data
  } catch (e) { /* */ }
})
</script>

<style scoped>
/* ====== 变量 ====== */
.header {
  --primary: #1A6B7A;
  --primary-light: #E8F4F7;
  --accent: #E8734A;
  --text: #1F2937;
  --text-secondary: #6B7280;
  --border: #E5E7EB;
}

/* ====== Header ====== */
.header {
  --nav-gray: #F5F6F8;
  background: var(--nav-gray);
  border-bottom: 1px solid #E6E8EB;
  border-top: 2px solid var(--accent);
  box-shadow:
    0 1px 0 rgba(0,0,0,0.03),
    0 2px 8px rgba(0,0,0,0.04);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-inner {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  padding: 0 20px;
  height: 56px;
  position: relative;
  flex-wrap: nowrap;
}

.logo {
  font-size: 22px; font-weight: 700; color: var(--primary);
  text-decoration: none; letter-spacing: 2px; margin-right: 24px;
  transition: opacity 0.25s; flex-shrink: 0;
}
.logo:hover { opacity: 0.8; }

/* ====== 导航链接 ====== */
.nav-links { display: flex; gap: 0; flex: 1; min-width: 0; }

.nav-item-wrapper { position: static; flex-shrink: 1; min-width: 0; }

.nav-item {
  position: relative;
  color: var(--text);
  text-decoration: none;
  font-size: 13px;
  padding: 6px 10px;
  border-radius: 6px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: inline-flex;
  align-items: center;
  gap: 4px;
  white-space: nowrap;
}

/* 下拉箭头图标 */
.nav-arrow-icon {
  font-size: 11px;
  transition: transform 0.3s;
}
.nav-item:hover .nav-arrow-icon {
  transform: rotate(180deg);
}

.nav-item:hover {
  color: var(--primary);
  background: var(--primary-light);
  transform: translateY(-1px);
}
.nav-item.router-link-active {
  color: var(--primary);
  font-weight: 600;
}

/* ====== 下拉面板 ====== */
.nav-dropdown-panel {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: rgba(255, 255, 255, 0.97);
  backdrop-filter: blur(16px) saturate(180%);
  -webkit-backdrop-filter: blur(16px) saturate(180%);
  box-shadow:
    0 8px 32px rgba(0, 0, 0, 0.08),
    0 0 0 1px rgba(0, 0, 0, 0.05);
  z-index: 99;
  display: flex;
  gap: 28px;
  padding: 24px 32px;
  max-width: 1200px;
  margin: 0 auto;
  border-radius: 0 0 12px 12px;
  animation: dropdownIn 0.22s cubic-bezier(0.25, 0.8, 0.25, 1);
}

@keyframes dropdownIn {
  from { opacity: 0; transform: translateY(-6px); }
  to   { opacity: 1; transform: translateY(0); }
}

.nav-dropdown-col {
  flex: 0 0 auto;
  min-width: 90px;
}

.nav-dropdown-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text);
  text-decoration: none;
  display: block;
  margin-bottom: 10px;
  padding-bottom: 8px;
  border-bottom: 2px solid var(--primary-light);
  transition: all 0.25s;
  white-space: nowrap;
}
.nav-dropdown-title:hover {
  color: var(--primary);
  border-bottom-color: var(--primary);
}

.nav-dropdown-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.nav-dropdown-tag {
  font-size: 12px;
  color: var(--text-secondary);
  text-decoration: none;
  padding: 3px 10px;
  background: #F5F6F8;
  border-radius: 4px;
  transition: all 0.25s cubic-bezier(0.25, 0.8, 0.25, 1);
  border: 1px solid transparent;
  white-space: nowrap;
}
.nav-dropdown-tag:hover {
  color: var(--accent);
  background: #FFF5F0;
  border-color: #FDE0D4;
  transform: scale(1.06);
}

/* ====== 用户区 ====== */
.header-actions { display: flex; align-items: center; gap: 6px; font-size: 13px; flex-shrink: 1; min-width: 0; }
.user-info {
  display: flex; align-items: center; gap: 8px;
  text-decoration: none; cursor: pointer; padding: 4px 8px;
  border-radius: 8px; transition: all 0.25s;
}
.user-info:hover { background: var(--primary-light); }
.user-avatar { border: 2px solid #E8F4F7; }
.user-avatar-default {
  background: var(--primary); color: #fff;
  font-size: 14px; font-weight: 600;
}
.user-name { color: var(--text-secondary); white-space: nowrap; transition: color 0.2s; }
.user-info:hover .user-name { color: var(--primary); }

.link {
  color: var(--text-secondary);
  text-decoration: none;
  padding: 6px 12px;
  border-radius: 4px;
  transition: all 0.25s;
}
.link:hover {
  color: var(--primary);
  background: var(--primary-light);
}

.divider { color: var(--border); }

.cart-link {
  position: relative;
  color: var(--text);
  padding: 7px 10px;
  border-radius: 8px;
  transition: all 0.25s;
  display: flex;
  align-items: center;
}
.cart-link:hover {
  background: var(--primary-light);
  color: var(--primary);
  transform: translateY(-1px);
}

.cart-badge {
  position: absolute;
  top: -2px; right: -4px;
  background: var(--accent);
  color: #fff;
  font-size: 10px; font-weight: 600;
  padding: 1px 5px;
  border-radius: 10px;
  min-width: 16px;
  text-align: center;
  transition: transform 0.2s;
}
.cart-link:hover .cart-badge {
  transform: scale(1.15);
}
</style>
