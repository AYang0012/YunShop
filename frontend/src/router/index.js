import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  // 前台
  { path: '/', name: 'home', component: () => import('@/views/front/Home.vue') },
  { path: '/login', name: 'login', component: () => import('@/views/front/Login.vue') },
  { path: '/register', name: 'register', component: () => import('@/views/front/Register.vue') },
  { path: '/goods/list', name: 'goodsList', component: () => import('@/views/front/GoodsList.vue') },
  { path: '/goods/detail/:id', name: 'goodsDetail', component: () => import('@/views/front/GoodsDetail.vue') },
  { path: '/cart', name: 'cart', component: () => import('@/views/front/Cart.vue') },
  { path: '/order/confirm', name: 'orderConfirm', component: () => import('@/views/front/OrderConfirm.vue') },
  { path: '/order/detail/:id', name: 'orderDetail', component: () => import('@/views/front/OrderDetail.vue') },
  { path: '/user', name: 'userCenter', component: () => import('@/views/front/UserCenter.vue') },
  { path: '/user/orders', name: 'userOrders', component: () => import('@/views/front/UserOrders.vue') },
  { path: '/user/address', name: 'userAddress', component: () => import('@/views/front/UserAddress.vue') },
  { path: '/user/profile', name: 'userProfile', component: () => import('@/views/front/UserProfile.vue') },
  { path: '/user/password', name: 'userPassword', component: () => import('@/views/front/UserPassword.vue') },

  // 后台
  { path: '/admin/login', name: 'adminLogin', component: () => import('@/views/admin/Login.vue') },
  {
    path: '/admin',
    component: () => import('@/views/admin/Index.vue'),
    children: [
      { path: '', name: 'adminIndex', component: () => import('@/views/admin/Dashboard.vue') },
      { path: 'goods', name: 'adminGoods', component: () => import('@/views/admin/GoodsList.vue') },
      { path: 'goods/edit/:id?', name: 'adminGoodsEdit', component: () => import('@/views/admin/GoodsEdit.vue') },
      { path: 'category', name: 'adminCategory', component: () => import('@/views/admin/CategoryList.vue') },
      { path: 'order', name: 'adminOrder', component: () => import('@/views/admin/OrderList.vue') },
      { path: 'user', name: 'adminUser', component: () => import('@/views/admin/UserList.vue') }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
