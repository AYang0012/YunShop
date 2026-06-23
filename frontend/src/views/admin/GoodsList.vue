<template>
  <div class="admin-page">
    <div class="page-head">
      <h1>商品管理</h1>
      <div>
        <el-button type="primary" @click="$router.push('/admin/goods/edit')">添加商品</el-button>
      </div>
    </div>
    <el-table :data="goodsList" stripe style="width: 100%">
      <el-table-column prop="goodsId" label="ID" width="60" />
      <el-table-column prop="goodsName" label="商品名称" min-width="200" />
      <el-table-column prop="shopPrice" label="售价" width="100" />
      <el-table-column prop="storeCount" label="库存" width="80" />
      <el-table-column prop="salesSum" label="销量" width="80" />
      <el-table-column label="状态" width="80">
        <template #default="{ row }">
          <el-tag :type="row.isOnSale === 1 ? 'success' : 'info'" size="small">{{ row.isOnSale === 1 ? '上架' : '下架' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-button size="small" @click="$router.push(`/admin/goods/edit/${row.goodsId}`)">编辑</el-button>
          <el-button size="small" :type="row.isOnSale === 1 ? 'warning' : 'success'"
            @click="toggleSale(row)">{{ row.isOnSale === 1 ? '下架' : '上架' }}</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination v-if="total > 0" background layout="prev, pager, next" :total="total" :page-size="pageSize" v-model:current-page="page" @change="fetchList" style="margin-top: 16px; justify-content: center;" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const goodsList = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(20)

const fetchList = async () => {
  try {
    const res = await axios.get('/api/goods/list', { params: { page: page.value, pageSize: pageSize.value } })
    if (res.data.code === 200) { goodsList.value = res.data.data.list; total.value = res.data.data.total }
  } catch (e) { /* */ }
}

const toggleSale = async (row) => {
  try {
    await axios.put(`/api/admin/goods/toggle/${row.goodsId}`)
    ElMessage.success('操作成功'); fetchList()
  } catch (e) { /* */ }
}

onMounted(fetchList)
</script>

<style scoped>
.admin-page { background: #fff; border-radius: 8px; padding: 20px; }
.page-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.page-head h1 { font-size: 20px; color: #1F2937; }
</style>
