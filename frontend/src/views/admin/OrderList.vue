<template>
  <div class="admin-page">
    <div class="page-head">
      <h1>订单管理</h1>
    </div>

    <!-- 筛选条件 -->
    <div class="filter-bar">
      <el-input v-model="filters.orderSn" placeholder="订单号" clearable style="width: 200px" @clear="fetchList" />
      <el-select v-model="filters.status" placeholder="订单状态" clearable style="width: 150px" @change="fetchList">
        <el-option label="待付款" value="PENDING" />
        <el-option label="已付款" value="PAID" />
        <el-option label="已发货" value="SHIPPED" />
        <el-option label="已完成" value="COMPLETED" />
        <el-option label="已取消" value="CANCELLED" />
        <el-option label="已退款" value="REFUNDED" />
      </el-select>
      <el-button type="primary" @click="fetchList">搜索</el-button>
    </div>

    <el-table :data="orderList" stripe style="width: 100%">
      <el-table-column prop="orderId" label="ID" width="60" />
      <el-table-column prop="orderSn" label="订单号" width="180" />
      <el-table-column label="买家" width="120">
        <template #default="{ row }">
          <span>{{ row.userNickname || '-' }}</span>
        </template>
      </el-table-column>
      <el-table-column label="订单金额" width="100">
        <template #default="{ row }">
          <span style="color: #F56C6C; font-weight: 600;">¥{{ row.totalAmount }}</span>
        </template>
      </el-table-column>
      <el-table-column label="支付方式" width="100">
        <template #default="{ row }">
          <span>{{ payNameMap[row.payName] || row.payName || '-' }}</span>
        </template>
      </el-table-column>
      <el-table-column label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="statusTypeMap[row.orderStatus]" size="small">{{ statusTextMap[row.orderStatus] }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="addTime" label="下单时间" width="170" />
      <el-table-column label="操作" width="240">
        <template #default="{ row }">
          <el-button size="small" @click="showDetail(row)">详情</el-button>
          <el-button v-if="row.orderStatus === 'PAID'" size="small" type="success" @click="handleShip(row)">发货</el-button>
          <el-button v-if="row.orderStatus === 'PAID' || row.orderStatus === 'SHIPPED'" size="small" type="warning" @click="handleRefund(row)">退款</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination v-if="total > 0" background layout="prev, pager, next, total" :total="total" :page-size="pageSize" v-model:current-page="page" @change="fetchList" style="margin-top: 16px; justify-content: center;" />

    <!-- 订单详情对话框 -->
    <el-dialog v-model="detailVisible" title="订单详情" width="700px">
      <template v-if="detailData">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="订单号">{{ detailData.order.orderSn }}</el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="statusTypeMap[detailData.order.orderStatus]" size="small">{{ statusTextMap[detailData.order.orderStatus] }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="买家">{{ detailData.user?.nickname || '-' }}</el-descriptions-item>
          <el-descriptions-item label="买家手机">{{ detailData.user?.mobile || '-' }}</el-descriptions-item>
          <el-descriptions-item label="订单金额">¥{{ detailData.order.totalAmount }}</el-descriptions-item>
          <el-descriptions-item label="运费">¥{{ detailData.order.shippingFee || '0.00' }}</el-descriptions-item>
          <el-descriptions-item label="支付方式">{{ payNameMap[detailData.order.payName] || detailData.order.payName || '-' }}</el-descriptions-item>
          <el-descriptions-item label="下单时间">{{ detailData.order.addTime }}</el-descriptions-item>
          <el-descriptions-item label="收货地址" :span="2">{{ detailData.order.addressSnapshot }}</el-descriptions-item>
          <el-descriptions-item label="备注" :span="2">{{ detailData.order.remark || '无' }}</el-descriptions-item>
        </el-descriptions>

        <h4 style="margin: 16px 0 8px; color: #1F2937;">商品明细</h4>
        <el-table :data="detailData.goodsList" stripe size="small">
          <el-table-column prop="goodsName" label="商品名称" />
          <el-table-column prop="goodsPrice" label="单价" width="100" />
          <el-table-column prop="goodsNum" label="数量" width="80" />
          <el-table-column label="小计" width="100">
            <template #default="{ row }">
              <span style="color: #F56C6C;">¥{{ (row.goodsPrice * row.goodsNum).toFixed(2) }}</span>
            </template>
          </el-table-column>
        </el-table>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getOrderList, getOrderDetail, shipOrder, refundOrder } from '@/api/admin'

const orderList = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(20)
const detailVisible = ref(false)
const detailData = ref(null)

const filters = reactive({
  orderSn: '',
  status: ''
})

const statusTextMap = {
  PENDING: '待付款',
  PAID: '已付款',
  SHIPPED: '已发货',
  COMPLETED: '已完成',
  CANCELLED: '已取消',
  RETURNING: '退货中',
  REFUNDED: '已退款'
}

const statusTypeMap = {
  PENDING: 'warning',
  PAID: 'primary',
  SHIPPED: 'success',
  COMPLETED: '',
  CANCELLED: 'info',
  RETURNING: 'danger',
  REFUNDED: 'danger'
}

const payNameMap = {
  alipay: '支付宝',
  wechat: '微信支付',
  unionpay: '银联',
  cod: '货到付款'
}

const fetchList = async () => {
  try {
    const params = {
      page: page.value,
      pageSize: pageSize.value,
      ...filters
    }
    // 移除空值
    Object.keys(params).forEach(key => {
      if (params[key] === '' || params[key] === null) delete params[key]
    })
    const res = await getOrderList(params)
    if (res.data.code === 200) {
      orderList.value = res.data.data.list
      total.value = res.data.data.total
    }
  } catch (e) { /* */ }
}

const showDetail = async (row) => {
  try {
    const res = await getOrderDetail(row.orderId)
    if (res.data.code === 200) {
      detailData.value = res.data.data
      detailVisible.value = true
    }
  } catch (e) {
    ElMessage.error('获取详情失败')
  }
}

const handleShip = async (row) => {
  try {
    await ElMessageBox.confirm(`确定对订单「${row.orderSn}」执行发货操作吗？`, '确认发货', { type: 'warning' })
    const res = await shipOrder(row.orderId)
    if (res.data.code === 200) {
      ElMessage.success('发货成功')
      fetchList()
    } else {
      ElMessage.error(res.data.msg)
    }
  } catch (e) { /* 取消 */ }
}

const handleRefund = async (row) => {
  try {
    await ElMessageBox.confirm(`确定对订单「${row.orderSn}」执行退款操作吗？此操作不可撤销。`, '确认退款', { type: 'warning' })
    const res = await refundOrder(row.orderId)
    if (res.data.code === 200) {
      ElMessage.success('退款成功')
      fetchList()
    } else {
      ElMessage.error(res.data.msg)
    }
  } catch (e) { /* 取消 */ }
}

onMounted(fetchList)
</script>

<style scoped>
.admin-page { background: #fff; border-radius: 8px; padding: 20px; }
.page-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.page-head h1 { font-size: 20px; color: #1F2937; }
.filter-bar { display: flex; gap: 12px; margin-bottom: 16px; }
</style>
