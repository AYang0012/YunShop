<template>
  <div class="order-detail-page">
    <header class="top-bar"><router-link to="/" class="logo">云集优选</router-link><span>订单详情</span></header>
    <div class="main" v-if="order">
      <div class="status-bar">
        <span class="status-label">{{ statusMap[order.orderStatus] || order.orderStatus }}</span>
        <span class="order-sn">订单号: {{ order.orderSn }}</span>
        <span class="order-time">{{ order.addTime }}</span>
      </div>
      <div class="section">
        <h3>商品信息</h3>
        <div v-for="g in goodsList" :key="g.id" class="g-row">
          <span>{{ g.goodsName }} <span v-if="g.goodsAttr" class="attr">[{{ g.goodsAttr }}]</span></span>
          <span>¥{{ g.goodsPrice }} × {{ g.goodsNum }}</span>
        </div>
      </div>
      <div class="section">
        <h3>金额</h3>
        <p>商品总额: ¥{{ order.totalAmount }} | 运费: ¥{{ order.shippingFee || '0.00' }}</p>
        <p class="total">实付: <b>¥{{ order.orderAmount }}</b></p>
      </div>
      <div class="actions">
        <el-button v-if="order.orderStatus === 'PENDING'" type="primary" @click="doPay">立即支付</el-button>
        <el-button v-if="order.orderStatus === 'PENDING'" @click="doCancel">取消订单</el-button>
        <el-button v-if="order.orderStatus === 'SHIPPED'" type="success" @click="doReceive">确认收货</el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getOrderDetail, payOrder, cancelOrder, confirmReceive } from '@/api/order'

const route = useRoute()
const router = useRouter()
const order = ref(null)
const goodsList = ref([])
const statusMap = { PENDING: '待付款', PAID: '待发货', SHIPPED: '已发货', COMPLETED: '已完成', CANCELLED: '已取消', RETURNING: '退货中', REFUNDED: '已退款' }

onMounted(async () => {
  try {
    const res = await getOrderDetail(route.params.id)
    if (res.code === 200) { order.value = res.data.order; goodsList.value = res.data.goodsList }
  } catch (e) { /* */ }
})

const doPay = async () => { await payOrder(order.value.orderId); ElMessage.success('支付成功'); router.go(0) }
const doCancel = async () => { await cancelOrder(order.value.orderId); ElMessage.success('已取消'); router.go(0) }
const doReceive = async () => { await confirmReceive(order.value.orderId); ElMessage.success('已确认收货'); router.go(0) }
</script>

<style scoped>
.order-detail-page { background: #FAFAF8; min-height: 100vh; }
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
.status-bar { background: #fff; border-radius: 12px; padding: 20px 24px; display: flex; align-items: center; gap: 24px; margin-bottom: 12px; }
.status-label { font-size: 18px; font-weight: 700; color: #E8734A; }
.order-sn { color: #6B7280; font-size: 13px; }
.order-time { color: #9CA3AF; font-size: 13px; margin-left: auto; }
.section { background: #fff; border-radius: 12px; padding: 20px 24px; margin-bottom: 12px; }
.section h3 { font-size: 16px; font-weight: 600; margin-bottom: 12px; color: #1F2937; }
.g-row { display: flex; justify-content: space-between; padding: 6px 0; font-size: 14px; color: #1F2937; }
.attr { color: #9CA3AF; font-size: 12px; }
.total { font-size: 18px; color: #E8734A; margin-top: 8px; }
.total b { font-size: 24px; }
.actions { display: flex; gap: 12px; padding: 16px 24px; background: #fff; border-radius: 12px; }
</style>
