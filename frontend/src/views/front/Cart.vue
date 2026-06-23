<template>
  <div class="cart-page">
    <header class="top-bar">
      <router-link to="/" class="logo">云集优选</router-link>
      <span class="title-text">我的购物车</span>
    </header>
    <div class="main" v-if="cartItems.length">
      <div class="cart-table">
        <div class="cart-header">
          <el-checkbox v-model="allSelected" @change="handleSelectAll" />
          <span class="col-name">商品名称</span><span class="col-price">单价</span>
          <span class="col-num">数量</span><span class="col-sub">小计</span><span class="col-act">操作</span>
        </div>
        <div v-for="item in cartItems" :key="item.cartId" class="cart-row">
          <el-checkbox :model-value="item.selected === 1" @change="toggleItem(item.cartId)" />
          <div class="col-name" @click="$router.push(`/goods/detail/${item.goodsId}`)">
            <span class="g-name">{{ item.goodsName }}</span>
            <span class="g-attr" v-if="item.attrInfo">{{ item.attrInfo }}</span>
          </div>
          <span class="col-price">¥{{ item.goodsPrice }}</span>
          <span class="col-num">
            <el-input-number v-model="item.goodsNum" :min="1" :max="200" size="small" @change="updateNum(item)" />
          </span>
          <span class="col-sub">¥{{ item.subtotal }}</span>
          <span class="col-act"><el-button text type="danger" @click="deleteItem(item.cartId)">删除</el-button></span>
        </div>
      </div>
      <div class="cart-footer">
        <el-button @click="deleteSelected" :disabled="!selectedIds.length">删除选中</el-button>
        <router-link to="/" class="keep-shop">继续购物</router-link>
        <div class="summary">
          <span>已选 <b>{{ selectedCount }}</b> 件</span>
          <span class="total">合计: <b>¥{{ totalPrice }}</b></span>
          <el-button type="primary" size="large" :disabled="!selectedCount" @click="$router.push('/order/confirm')">去结算</el-button>
        </div>
      </div>
    </div>
    <el-empty v-else description="购物车还没有任何商品，马上去购物">
      <el-button type="primary" @click="$router.push('/')">去逛逛</el-button>
    </el-empty>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getCartList, updateCartNum, deleteCartItem, deleteCartBatch, toggleCartItem, selectAll } from '@/api/cart'

const cartItems = ref([])

const allSelected = computed(() => cartItems.value.length > 0 && cartItems.value.every(i => i.selected === 1))
const selectedCount = computed(() => cartItems.value.filter(i => i.selected === 1).reduce((s, i) => s + i.goodsNum, 0))
const totalPrice = computed(() => cartItems.value.filter(i => i.selected === 1).reduce((s, i) => s + i.subtotal, 0))
const selectedIds = computed(() => cartItems.value.filter(i => i.selected === 1).map(i => i.cartId))

const fetchList = async () => {
  try {
    const res = await getCartList()
    if (res.code === 200) cartItems.value = res.data
  } catch (e) { /* */ }
}

const handleSelectAll = async (val) => {
  try { await selectAll(val); fetchList() } catch (e) { /* */ }
}

const toggleItem = async (cartId) => {
  try { await toggleCartItem(cartId); fetchList() } catch (e) { /* */ }
}

const updateNum = async (item) => {
  try { await updateCartNum(item.cartId, item.goodsNum); fetchList() } catch (e) { /* */ }
}

const deleteItem = async (cartId) => {
  try { await deleteCartItem(cartId); ElMessage.success('已删除'); fetchList() } catch (e) { /* */ }
}

const deleteSelected = async () => {
  try {
    await ElMessageBox.confirm('确定删除选中的商品吗？', '提示', { type: 'warning' })
    await deleteCartBatch(selectedIds.value)
    ElMessage.success('已删除')
    fetchList()
  } catch (e) { /* */ }
}

onMounted(fetchList)
</script>

<style scoped>
.cart-page { background: #FAFAF8; min-height: 100vh; }
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
.title-text { font-size: 16px; color: #1F2937; }
.main { max-width: 1200px; margin: 0 auto; padding: 0 20px; }
.cart-table { background: #fff; border-radius: 12px; padding: 16px 24px; }
.cart-header, .cart-row { display: grid; grid-template-columns: 40px 1fr 120px 140px 120px 80px; align-items: center; padding: 12px 0; gap: 12px; font-size: 14px; }
.cart-header { color: #6B7280; border-bottom: 1px solid #E5E7EB; }
.cart-row { border-bottom: 1px solid #F3F4F6; }
.col-name { cursor: pointer; }
.g-name { display: block; color: #1F2937; }
.g-attr { font-size: 12px; color: #9CA3AF; }
.col-price, .col-sub { color: #E8734A; font-weight: 600; }
.cart-footer { display: flex; align-items: center; gap: 16px; padding: 16px 24px; background: #fff; margin-top: 12px; border-radius: 12px; }
.keep-shop { color: #6B7280; text-decoration: none; font-size: 13px; }
.summary { margin-left: auto; display: flex; align-items: center; gap: 16px; }
.total { font-size: 18px; color: #E8734A; }
.total b { font-size: 22px; }
</style>
