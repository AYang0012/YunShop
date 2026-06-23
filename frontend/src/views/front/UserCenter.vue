<template>
  <div class="user-page">
    <header class="top-bar">
      <router-link to="/" class="logo">云集优选</router-link>
      <span>用户中心</span>
      <router-link to="/" class="home-link">返回首页</router-link>
    </header>
    <div class="main">
      <aside class="sidebar">
        <div class="user-info">
          <div class="avatar">
            <img v-if="user?.avatar" :src="user.avatar" class="avatar-img" alt="头像" />
            <el-icon v-else :size="40"><UserFilled /></el-icon>
          </div>
          <p class="nickname">{{ user?.nickname || '用户' }}</p>
        </div>
        <nav class="side-nav">
          <router-link to="/user/orders" class="nav-item">我的订单</router-link>
          <router-link to="/user/address" class="nav-item">收货地址</router-link>
          <router-link to="/user/profile" class="nav-item">个人信息</router-link>
          <router-link to="/user/password" class="nav-item">修改密码</router-link>
        </nav>
      </aside>
      <div class="content">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getCurrentUser } from '@/api/user'

const user = ref(null)

onMounted(async () => {
  try { const r = await getCurrentUser(); if (r.code === 200) user.value = r.data } catch (e) { /* */ }
})
</script>

<style scoped>
.user-page { background: #FAFAF8; min-height: 100vh; }
.top-bar {
  max-width: 100%; margin: 0; display: flex; align-items: center;
  padding: 0 20px; height: 56px; gap: 16px;
  background: #F5F6F8; border-bottom: 1px solid #E6E8EB;
  border-top: 2px solid #E8734A;
  box-shadow: 0 1px 0 rgba(0,0,0,0.03), 0 2px 8px rgba(0,0,0,0.04);
  position: sticky; top: 0; z-index: 100;
}
.logo { font-size: 20px; font-weight: 700; color: #1A6B7A; text-decoration: none; transition: opacity 0.25s; }
.logo:hover { opacity: 0.8; }
.home-link { margin-left: auto; color: #6B7280; text-decoration: none; font-size: 13px; }
.main { max-width: 1200px; margin: 0 auto; padding: 16px 20px; display: flex; gap: 16px; }
.sidebar { width: 220px; background: #fff; border-radius: 12px; padding: 16px; align-self: flex-start; }
.user-info { text-align: center; padding-bottom: 16px; border-bottom: 1px solid #E5E7EB; }
.avatar { width: 64px; height: 64px; border-radius: 50%; background: #E8F4F7; display: flex; align-items: center; justify-content: center; margin: 0 auto; color: #1A6B7A; overflow: hidden; }
.avatar-img { width: 100%; height: 100%; object-fit: cover; }
.nickname { margin-top: 8px; font-weight: 600; color: #1F2937; }
.side-nav { margin-top: 8px; }
.nav-item { display: block; padding: 10px 12px; color: #1F2937; text-decoration: none; font-size: 14px; border-radius: 6px; transition: all .2s; }
.nav-item:hover, .nav-item.router-link-active { background: #E8F4F7; color: #1A6B7A; }
.content { flex: 1; background: #fff; border-radius: 12px; padding: 24px; min-height: 400px; }
</style>
