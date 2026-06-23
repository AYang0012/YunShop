<template>
  <div class="detail-page">
    <header class="top-bar">
      <router-link to="/" class="logo">云集优选</router-link>
      <router-link to="/cart" class="cart-btn"><el-icon :size="24"><ShoppingCart /></el-icon></router-link>
    </header>
    <div class="main" v-if="goods">
      <div class="detail-top">
        <div class="gallery"><img :src="goods.goodsThumb || `/api/images/goods/${goods.goodsId}`" :alt="goods.goodsName" class="main-img" /></div>
        <div class="info">
          <h1 class="goods-title">{{ goods.goodsName }}</h1>
          <p class="desc">{{ goods.keywords }}</p>
          <div class="price-box">
            <span class="shop-price">¥{{ goods.shopPrice }}</span>
            <span class="market-price" v-if="goods.marketPrice > goods.shopPrice">¥{{ goods.marketPrice }}</span>
          </div>
          <div class="meta"><span>销量: {{ goods.salesSum }}</span><span>库存: {{ goods.storeCount }}</span></div>
          <div class="actions">
            <el-input-number v-model="buyNum" :min="1" :max="goods.storeCount" size="large" />
            <el-button type="primary" size="large" @click="addToCart">加入购物车</el-button>
            <el-button type="danger" size="large" @click="buyNow">立即购买</el-button>
          </div>
        </div>
      </div>
      <div class="detail-content">
        <h3>商品详情</h3>
        <div v-html="goods.goodsContent || '<p>暂无详情</p>'"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getGoodsDetail } from '@/api/goods'
import { addToCart as apiAddToCart } from '@/api/cart'

const route = useRoute()
const router = useRouter()
const goods = ref(null)
const images = ref([])
const buyNum = ref(1)

onMounted(async () => {
  try {
    const res = await getGoodsDetail(route.params.id)
    if (res.code === 200) {
      goods.value = res.data.goods
      images.value = res.data.images
    }
  } catch (e) { /* */ }
})

const addToCart = async () => {
  try {
    await apiAddToCart(goods.value.goodsId, buyNum.value)
    ElMessage.success('已加入购物车')
  } catch (e) { /* */ }
}

const buyNow = async () => {
  await addToCart()
  router.push('/cart')
}
</script>

<style scoped>
.detail-page { background: #FAFAF8; min-height: 100vh; }
.top-bar {
  max-width: 100%; margin: 0; display: flex; align-items: center;
  justify-content: space-between;
  padding: 0 20px; height: 56px;
  background: #F5F6F8; border-bottom: 1px solid #E6E8EB;
  border-top: 2px solid #E8734A;
  box-shadow: 0 1px 0 rgba(0,0,0,0.03), 0 2px 8px rgba(0,0,0,0.04);
  position: sticky; top: 0; z-index: 100;
}
.logo { font-size: 20px; font-weight: 700; color: #1A6B7A; text-decoration: none; transition: opacity 0.25s; }
.logo:hover { opacity: 0.8; }
.cart-btn { color: #1F2937; }
.main { max-width: 1200px; margin: 0 auto; padding: 0 20px; }
.detail-top { display: flex; gap: 32px; background: #fff; padding: 32px; border-radius: 12px; }
.gallery { flex: 1; }
.main-img { width: 100%; height: 400px; object-fit: cover; border-radius: 8px; }
.info { flex: 1; }
.goods-title { font-size: 22px; font-weight: 700; color: #1F2937; }
.desc { color: #9CA3AF; font-size: 13px; margin: 8px 0; }
.price-box { background: #FFF5F0; padding: 16px; border-radius: 8px; margin: 16px 0; }
.shop-price { font-size: 28px; font-weight: 700; color: #E8734A; }
.market-price { font-size: 14px; color: #9CA3AF; text-decoration: line-through; margin-left: 12px; }
.meta { display: flex; gap: 24px; color: #6B7280; font-size: 13px; margin: 12px 0; }
.actions { display: flex; gap: 12px; align-items: center; margin-top: 20px; }
.detail-content { background: #fff; margin-top: 16px; padding: 24px 32px; border-radius: 12px; }
.detail-content h3 { font-size: 18px; color: #1F2937; margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid #E5E7EB; }
</style>
