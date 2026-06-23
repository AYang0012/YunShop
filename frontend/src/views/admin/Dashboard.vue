<template>
  <div class="admin-page">
    <div class="page-head">
      <h1>仪表盘</h1>
      <span style="color:#6B7280; font-size:14px;">欢迎使用云集优选后台管理系统</span>
    </div>

    <el-row :gutter="20" style="margin-top: 24px;">
      <el-col :span="6">
        <div class="stat-card">
          <div class="stat-icon" style="background: #EBF5FF;">
            <el-icon :size="32" color="#3B82F6"><Goods /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.goodsCount }}</div>
            <div class="stat-label">商品总数</div>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card">
          <div class="stat-icon" style="background: #FEF3C7;">
            <el-icon :size="32" color="#F59E0B"><Document /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.orderCount }}</div>
            <div class="stat-label">订单总数</div>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card">
          <div class="stat-icon" style="background: #D1FAE5;">
            <el-icon :size="32" color="#10B981"><User /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.userCount }}</div>
            <div class="stat-label">注册会员</div>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card">
          <div class="stat-icon" style="background: #FCE7F3;">
            <el-icon :size="32" color="#EC4899"><TrendCharts /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">¥{{ stats.totalSales }}</div>
            <div class="stat-label">总销售额</div>
          </div>
        </div>
      </el-col>
    </el-row>

    <div class="panel" style="margin-top: 24px;">
      <h3 style="margin-bottom: 16px; color: #1F2937;">快捷入口</h3>
      <el-row :gutter="16">
        <el-col :span="6">
          <div class="quick-link" @click="$router.push('/admin/goods')">
            <el-icon :size="24"><Plus /></el-icon>
            <span>添加商品</span>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="quick-link" @click="$router.push('/admin/order')">
            <el-icon :size="24"><Document /></el-icon>
            <span>查看订单</span>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="quick-link" @click="$router.push('/admin/category')">
            <el-icon :size="24"><Menu /></el-icon>
            <span>管理分类</span>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="quick-link" @click="$router.push('/admin/user')">
            <el-icon :size="24"><User /></el-icon>
            <span>会员管理</span>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const stats = ref({
  goodsCount: 0,
  orderCount: 0,
  userCount: 0,
  totalSales: 0
})

const fetchStats = async () => {
  try {
    const res = await axios.get('/api/admin/stats')
    if (res.data.code === 200) {
      stats.value = res.data.data
    }
  } catch (e) {
    // 使用默认值
    stats.value = { goodsCount: 0, orderCount: 0, userCount: 0, totalSales: 0 }
  }
}

onMounted(fetchStats)
</script>

<style scoped>
.admin-page { background: #fff; border-radius: 8px; padding: 20px; min-height: calc(100vh - 48px); }
.page-head { margin-bottom: 8px; }
.page-head h1 { font-size: 20px; color: #1F2937; }

.stat-card {
  display: flex; align-items: center; gap: 16px;
  background: #fff; border: 1px solid #E5E7EB; border-radius: 8px; padding: 20px;
}
.stat-icon { width: 56px; height: 56px; border-radius: 12px; display: flex; align-items: center; justify-content: center; }
.stat-value { font-size: 24px; font-weight: 600; color: #1F2937; }
.stat-label { font-size: 13px; color: #6B7280; margin-top: 4px; }

.panel { background: #fff; border: 1px solid #E5E7EB; border-radius: 8px; padding: 20px; }
.quick-link {
  display: flex; flex-direction: column; align-items: center; gap: 8px;
  padding: 24px; border: 1px dashed #D1D5DB; border-radius: 8px; cursor: pointer;
  color: #6B7280; transition: all .2s;
}
.quick-link:hover { border-color: #3B82F6; color: #3B82F6; background: #F9FAFB; }
</style>
