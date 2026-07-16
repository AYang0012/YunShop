<template>
  <div class="admin-page">
    <div class="page-head">
      <h1>会员管理</h1>
    </div>

    <!-- 筛选条件 -->
    <div class="filter-bar">
      <el-input v-model="filters.keyword" placeholder="昵称/手机号/邮箱" clearable style="width: 220px" @clear="fetchList" />
      <el-select v-model="filters.status" placeholder="状态" clearable style="width: 120px" @change="fetchList">
        <el-option label="正常" :value="1" />
        <el-option label="禁用" :value="0" />
      </el-select>
      <el-button type="primary" @click="fetchList">搜索</el-button>
    </div>

    <el-table :data="userList" stripe style="width: 100%">
      <el-table-column prop="userId" label="ID" width="60" />
      <el-table-column label="会员信息" min-width="200">
        <template #default="{ row }">
          <div style="display: flex; align-items: center; gap: 8px;">
            <el-avatar :size="32" :src="row.avatar">{{ (row.nickname || '?')[0] }}</el-avatar>
            <div>
              <div style="font-weight: 500;">{{ row.nickname || '-' }}</div>
              <div style="font-size: 12px; color: #6B7280;">{{ row.mobile || row.email }}</div>
            </div>
          </div>
        </template>
      </el-table-column>
      <el-table-column prop="level" label="等级" width="80">
        <template #default="{ row }">
          <el-tag size="small">Lv.{{ row.level }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="points" label="积分" width="80" />
      <el-table-column label="状态" width="80">
        <template #default="{ row }">
          <el-tag :type="row.status === 1 ? 'success' : 'danger'" size="small">{{ row.status === 1 ? '正常' : '禁用' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="regTime" label="注册时间" width="170" />
      <el-table-column prop="lastLogin" label="最后登录" width="170" />
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-button size="small" @click="showDetail(row)">详情</el-button>
          <el-button size="small" :type="row.status === 1 ? 'danger' : 'success'" @click="handleToggle(row)">
            {{ row.status === 1 ? '禁用' : '启用' }}
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination v-if="total > 0" background layout="prev, pager, next, total" :total="total" :page-size="pageSize" v-model:current-page="page" @change="fetchList" style="margin-top: 16px; justify-content: center;" />

    <!-- 会员详情对话框 -->
    <el-dialog v-model="detailVisible" title="会员详情" width="500px">
      <template v-if="detailData">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="ID">{{ detailData.userId }}</el-descriptions-item>
          <el-descriptions-item label="昵称">{{ detailData.nickname || '-' }}</el-descriptions-item>
          <el-descriptions-item label="手机号">{{ detailData.mobile || '-' }}</el-descriptions-item>
          <el-descriptions-item label="邮箱">{{ detailData.email || '-' }}</el-descriptions-item>
          <el-descriptions-item label="等级">Lv.{{ detailData.level }}</el-descriptions-item>
          <el-descriptions-item label="积分">{{ detailData.points }}</el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="detailData.status === 1 ? 'success' : 'danger'" size="small">{{ detailData.status === 1 ? '正常' : '禁用' }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="注册时间">{{ detailData.regTime }}</el-descriptions-item>
          <el-descriptions-item label="最后登录" :span="2">{{ detailData.lastLogin || '-' }}</el-descriptions-item>
        </el-descriptions>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getUserList, getUserDetail, toggleUserStatus } from '@/api/admin'

const userList = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(20)
const detailVisible = ref(false)
const detailData = ref(null)

const filters = reactive({
  keyword: '',
  status: null
})

const fetchList = async () => {
  try {
    const params = {
      page: page.value,
      pageSize: pageSize.value,
      ...filters
    }
    Object.keys(params).forEach(key => {
      if (params[key] === '' || params[key] === null) delete params[key]
    })
    const res = await getUserList(params)
    if (res.data.code === 200) {
      userList.value = res.data.data.list
      total.value = res.data.data.total
    }
  } catch (e) { /* */ }
}

const showDetail = async (row) => {
  try {
    const res = await getUserDetail(row.userId)
    if (res.data.code === 200) {
      detailData.value = res.data.data
      detailVisible.value = true
    }
  } catch (e) {
    ElMessage.error('获取详情失败')
  }
}

const handleToggle = async (row) => {
  const action = row.status === 1 ? '禁用' : '启用'
  try {
    await ElMessageBox.confirm(`确定${action}会员「${row.nickname || row.mobile}」吗？`, '提示', { type: 'warning' })
    const res = await toggleUserStatus(row.userId)
    if (res.data.code === 200) {
      ElMessage.success(res.data.msg)
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
