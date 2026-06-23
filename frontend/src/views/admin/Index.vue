<template>
  <div class="admin-layout">
    <aside class="sidebar">
      <h2 class="sidebar-title">云集优选后台</h2>
      <nav class="side-menu">
        <router-link to="/admin" class="menu-item">仪表盘</router-link>
        <router-link to="/admin/goods" class="menu-item">商品管理</router-link>
        <router-link to="/admin/category" class="menu-item">分类管理</router-link>
        <router-link to="/admin/order" class="menu-item">订单管理</router-link>
        <router-link to="/admin/user" class="menu-item">会员管理</router-link>
      </nav>
    </aside>
    <main class="content">
      <router-view />
    </main>
  </div>
</template>

<style scoped>
.admin-layout { display: flex; min-height: 100vh; background: #F3F4F6; }
.sidebar { width: 220px; background: #1F2937; color: #fff; padding: 20px 0; flex-shrink: 0; }
.sidebar-title { font-size: 18px; padding: 0 20px 20px; border-bottom: 1px solid #374151; margin-bottom: 12px; letter-spacing: 2px; }
.side-menu { display: flex; flex-direction: column; }
.menu-item { padding: 12px 20px; color: #D1D5DB; text-decoration: none; font-size: 14px; transition: all .2s; }
.menu-item:hover, .menu-item.router-link-exact-active { background: #374151; color: #fff; }
.content { flex: 1; padding: 24px; overflow-y: auto; }
</style>
