<template>
  <div class="confirm-page">
    <header class="top-bar"><router-link to="/" class="logo">云集优选</router-link><span>确认订单</span></header>
    <div class="main">
      <!-- 收货地址 -->
      <div class="section">
        <h3>收货地址</h3>
        <div v-if="addresses.length" class="addr-list">
          <div v-for="addr in addresses" :key="addr.addressId"
            class="addr-item" :class="{ selected: selectedAddr === addr.addressId }"
            @click="selectedAddr = addr.addressId">
            <div class="addr-info">
              <span class="addr-name">{{ addr.consignee }}</span>
              <span class="addr-phone">{{ addr.mobile }}</span>
              <span class="addr-tag" v-if="addr.isDefault === 1">默认</span>
            </div>
            <p class="addr-detail">{{ addr.province }}{{ addr.city }}{{ addr.district }} {{ addr.address }}</p>
          </div>
        </div>
        <el-empty v-else description="暂无收货地址，请先添加" />
      </div>
      <!-- 商品清单 -->
      <div class="section">
        <h3>商品清单</h3>
        <div v-for="item in cartItems" :key="item.cartId" class="goods-row" v-show="item.selected === 1">
          <span class="g-name">{{ item.goodsName }}</span>
          <span class="g-price">¥{{ item.goodsPrice }} × {{ item.goodsNum }}</span>
          <span class="g-sub">¥{{ item.subtotal }}</span>
        </div>
      </div>
      <!-- 支付方式 -->
      <div class="section">
        <h3>支付方式</h3>
        <el-radio-group v-model="payName">
          <el-radio value="alipay">支付宝</el-radio>
          <el-radio value="wechat">微信支付</el-radio>
          <el-radio value="cod">货到付款</el-radio>
        </el-radio-group>
      </div>
      <!-- 备注 -->
      <div class="section">
        <el-input v-model="remark" placeholder="订单备注（选填）" maxlength="200" show-word-limit />
      </div>
      <!-- 提交 -->
      <div class="submit-bar">
        <span class="total">应付: <b>¥{{ totalPrice }}</b></span>
        <el-button type="primary" size="large" :disabled="!selectedAddr" @click="submitOrder">提交订单</el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getCartList } from '@/api/cart'
import { getAddressList } from '@/api/address'
import { submitOrder as apiSubmit } from '@/api/order'

const router = useRouter()
const cartItems = ref([])
const addresses = ref([])
const selectedAddr = ref(null)
const payName = ref('alipay')
const remark = ref('')

const totalPrice = computed(() =>
  cartItems.value.filter(i => i.selected === 1).reduce((s, i) => s + i.subtotal, 0)
)

onMounted(async () => {
  try { const r = await getCartList(); if (r.code === 200) cartItems.value = r.data } catch (e) { /* */ }
  try { const r = await getAddressList(); if (r.code === 200) {
    addresses.value = r.data
    const def = r.data.find(a => a.isDefault === 1)
    if (def) selectedAddr.value = def.addressId
    else if (r.data.length) selectedAddr.value = r.data[0].addressId
  }} catch (e) { /* */ }
})

const submitOrder = async () => {
  try {
    const res = await apiSubmit({ addressId: selectedAddr.value, payName: payName.value, remark: remark.value })
    ElMessage.success(res.msg || '下单成功')
    router.push(`/order/detail/${res.data.orderId}`)
  } catch (e) { /* */ }
}
</script>

<style scoped>
.confirm-page { background: #FAFAF8; min-height: 100vh; }
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
.main { max-width: 1200px; margin: 0 auto; padding: 0 20px; }
.section { background: #fff; border-radius: 12px; padding: 20px 24px; margin-bottom: 12px; }
.section h3 { font-size: 16px; font-weight: 600; color: #1F2937; margin-bottom: 12px; }
.addr-list { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
.addr-item { border: 2px solid #E5E7EB; border-radius: 8px; padding: 12px; cursor: pointer; transition: all .2s; }
.addr-item.selected { border-color: #1A6B7A; background: #E8F4F7; }
.addr-info { display: flex; align-items: center; gap: 8px; }
.addr-name { font-weight: 600; }
.addr-phone { color: #6B7280; font-size: 13px; }
.addr-tag { font-size: 11px; background: #E8734A; color: #fff; padding: 1px 6px; border-radius: 3px; }
.addr-detail { color: #6B7280; font-size: 13px; margin-top: 6px; }
.goods-row { display: flex; align-items: center; padding: 8px 0; border-bottom: 1px solid #F3F4F6; }
.g-name { flex: 1; }
.g-price { width: 200px; color: #6B7280; text-align: right; }
.g-sub { width: 120px; color: #E8734A; font-weight: 600; text-align: right; }
.submit-bar { display: flex; align-items: center; justify-content: flex-end; gap: 20px; padding: 20px 24px; background: #fff; border-radius: 12px; }
.total { font-size: 20px; color: #E8734A; }
.total b { font-size: 26px; }
</style>
