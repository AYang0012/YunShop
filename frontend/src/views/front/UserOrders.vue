<template>
  <div class="orders-page">
    <div class="page-card">
      <h1 class="page-title">我的订单</h1>
      <p class="page-desc">跟踪和管理您的每一笔订单</p>

      <!-- 筛选标签 -->
      <div class="tabs">
        <button v-for="tab in tabs" :key="tab.key"
          class="tab-btn" :class="{ active: activeTab === tab.key }"
          @click="activeTab = tab.key; fetchOrders()">
          {{ tab.label }}
          <span v-if="tab.key === activeTab" class="tab-dot"></span>
        </button>
      </div>

      <!-- 订单列表 -->
      <div v-if="orders.length" class="order-list">
        <div v-for="order in orders" :key="order.orderId" class="order-card"
          @click="$router.push(`/order/detail/${order.orderId}`)">
          <div class="order-header">
            <div class="order-meta">
              <span class="order-sn">{{ order.orderSn }}</span>
              <span class="order-time">{{ order.addTime }}</span>
            </div>
            <div class="order-status-row">
              <span class="status-dot" :class="order.orderStatus"></span>
              <span class="status-text" :class="order.orderStatus">{{ statusMap[order.orderStatus] }}</span>
            </div>
          </div>
          <div class="order-footer">
            <span class="order-amount">&yen;{{ order.orderAmount }}</span>
            <div class="order-actions" @click.stop>
              <el-button v-if="order.orderStatus === 'PENDING'" size="small" round @click="doPay(order.orderId)">
                立即支付
              </el-button>
              <el-button v-if="order.orderStatus === 'PENDING'" size="small" round plain @click="doCancel(order.orderId)">
                取消
              </el-button>
              <el-button v-if="order.orderStatus === 'SHIPPED'" size="small" round type="success" @click="doReceive(order.orderId)">
                确认收货
              </el-button>
            </div>
          </div>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-else class="empty-state">
        <el-icon :size="48" color="#D1D5DB"><Document /></el-icon>
        <p>暂无订单</p>
        <router-link to="/" class="shop-link">去逛逛</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Document } from '@element-plus/icons-vue'
import { getOrderList, payOrder, cancelOrder, confirmReceive } from '@/api/order'

const tabs = [
  { key: '', label: '全部' },
  { key: 'PENDING', label: '待付款' },
  { key: 'PAID', label: '待发货' },
  { key: 'SHIPPED', label: '已发货' },
  { key: 'COMPLETED', label: '已完成' }
]
const statusMap = {
  PENDING: '待付款', PAID: '待发货', SHIPPED: '已发货',
  COMPLETED: '已完成', CANCELLED: '已取消'
}
const activeTab = ref('')
const orders = ref([])

const fetchOrders = async () => {
  try {
    const r = await getOrderList(activeTab.value || undefined)
    if (r.code === 200) orders.value = r.data
  } catch { /* */ }
}
const doPay = async (id) => { await payOrder(id); ElMessage.success('支付成功'); fetchOrders() }
const doCancel = async (id) => { await cancelOrder(id); ElMessage.success('已取消'); fetchOrders() }
const doReceive = async (id) => { await confirmReceive(id); ElMessage.success('已确认收货'); fetchOrders() }

onMounted(fetchOrders)
</script>

<style scoped>
/* ====== Page ====== */
.orders-page {
  min-height: calc(100vh - 56px);
  background: linear-gradient(180deg, #F5F4F1 0%, #F0EFEC 100%);
  padding: 40px 20px 80px;
}

.page-card {
  max-width: 720px;
  margin: 0 auto;
  background: #fff;
  border-radius: 16px;
  padding: 40px;
  box-shadow: 0 1px 0 rgba(0,0,0,0.04), 0 4px 24px rgba(0,0,0,0.05), 0 16px 64px rgba(0,0,0,0.03);
  animation: cardIn 0.5s cubic-bezier(0.22, 0.61, 0.36, 1);
}
@keyframes cardIn {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0); }
}

.page-title {
  font-family: Georgia, 'Times New Roman', serif;
  font-size: 26px; font-weight: 400; color: #1F2937;
  margin: 0 0 4px; letter-spacing: 0.5px;
}
.page-desc { font-size: 13px; color: #9CA3AF; margin: 0 0 28px; }

/* ====== Tabs ====== */
.tabs { display: flex; gap: 4px; margin-bottom: 24px; }
.tab-btn {
  position: relative;
  padding: 8px 18px;
  border: none; background: transparent;
  font-size: 13px; color: #6B7280;
  cursor: pointer; border-radius: 20px;
  transition: all 0.25s;
  font-family: inherit;
}
.tab-btn:hover { color: #1F2937; background: #F5F6F8; }
.tab-btn.active { color: #1A6B7A; background: #E8F4F7; font-weight: 500; }
.tab-dot {
  position: absolute; bottom: 2px; left: 50%; transform: translateX(-50%);
  width: 4px; height: 4px; border-radius: 50%; background: #1A6B7A;
}

/* ====== Order Card ====== */
.order-list { display: flex; flex-direction: column; gap: 10px; }
.order-card {
  padding: 18px 20px;
  border: 1px solid #EAEAE8; border-radius: 12px;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.22, 0.61, 0.36, 1);
}
.order-card:hover { border-color: #D1D5DB; box-shadow: 0 2px 12px rgba(0,0,0,0.04); transform: translateY(-1px); }

.order-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; }
.order-meta { display: flex; flex-direction: column; gap: 2px; }
.order-sn { font-size: 14px; font-weight: 500; color: #1F2937; letter-spacing: 0.3px; }
.order-time { font-size: 12px; color: #9CA3AF; }

.order-status-row { display: flex; align-items: center; gap: 6px; }
.status-dot { width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0; }
.status-dot.PENDING { background: #F59E0B; }
.status-dot.PAID { background: #1A6B7A; }
.status-dot.SHIPPED { background: #6366F1; }
.status-dot.COMPLETED { background: #10B981; }
.status-dot.CANCELLED { background: #D1D5DB; }
.status-text { font-size: 13px; font-weight: 500; }
.status-text.PENDING { color: #F59E0B; }
.status-text.PAID { color: #1A6B7A; }
.status-text.SHIPPED { color: #6366F1; }
.status-text.COMPLETED { color: #10B981; }
.status-text.CANCELLED { color: #D1D5DB; }

.order-footer { display: flex; justify-content: space-between; align-items: center; }
.order-amount { font-size: 18px; font-weight: 600; color: #1F2937; letter-spacing: -0.3px; }
.order-actions { display: flex; gap: 8px; }

/* ====== Empty ====== */
.empty-state { text-align: center; padding: 48px 0; }
.empty-state p { color: #9CA3AF; margin: 12px 0 16px; font-size: 14px; }
.shop-link { color: #1A6B7A; text-decoration: none; font-size: 14px; font-weight: 500; }
.shop-link:hover { color: #E8734A; }

@media (max-width: 480px) {
  .orders-page { padding: 20px 12px 60px; }
  .page-card { padding: 24px 18px; }
}
</style>
