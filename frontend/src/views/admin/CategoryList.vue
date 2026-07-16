<template>
  <div class="admin-page">
    <div class="page-head">
      <h1>分类管理</h1>
      <el-button type="primary" @click="openAddDialog">添加分类</el-button>
    </div>

    <el-table :data="treeData" stripe row-key="id" :tree-props="{ children: 'children' }" default-expand-all style="width: 100%">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="name" label="分类名称" min-width="200" />
      <el-table-column prop="level" label="层级" width="80">
        <template #default="{ row }">
          <el-tag size="small">{{ row.level === 1 ? '一级' : row.level === 2 ? '二级' : '三级' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="sortOrder" label="排序" width="80" />
      <el-table-column label="显示" width="80">
        <template #default="{ row }">
          <el-switch :model-value="row.isShow === 1" @change="toggleShow(row)" />
        </template>
      </el-table-column>
      <el-table-column label="热门" width="80">
        <template #default="{ row }">
          <el-tag :type="row.isHot === 1 ? 'danger' : 'info'" size="small">{{ row.isHot === 1 ? '是' : '否' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-button size="small" @click="openEditDialog(row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 添加/编辑对话框 -->
    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑分类' : '添加分类'" width="500px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="分类名称">
          <el-input v-model="form.name" placeholder="请输入分类名称" />
        </el-form-item>
        <el-form-item label="父级分类">
          <el-select v-model="form.parentId" placeholder="无（一级分类）" clearable style="width: 100%">
            <el-option :value="0" label="无（一级分类）" />
            <el-option v-for="cat in flatCategories" :key="cat.id" :value="cat.id" :label="cat.displayName" />
          </el-select>
        </el-form-item>
        <el-form-item label="排序">
          <el-input-number v-model="form.sortOrder" :min="0" :max="999" />
        </el-form-item>
        <el-form-item label="显示">
          <el-switch v-model="form.isShow" :active-value="1" :inactive-value="0" />
        </el-form-item>
        <el-form-item label="热门">
          <el-switch v-model="form.isHot" :active-value="1" :inactive-value="0" />
        </el-form-item>
        <el-form-item label="图片">
          <el-input v-model="form.image" placeholder="图片URL（可选）" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getCategoryList, addCategory, updateCategory, deleteCategory, toggleCategoryShow } from '@/api/admin'

const categories = ref([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const submitting = ref(false)

const form = ref({
  id: null,
  name: '',
  parentId: 0,
  level: 1,
  sortOrder: 0,
  isShow: 1,
  isHot: 0,
  image: ''
})

// 构建树形结构
const treeData = computed(() => {
  const map = {}
  const roots = []
  categories.value.forEach(cat => {
    map[cat.id] = { ...cat, children: [] }
  })
  categories.value.forEach(cat => {
    if (cat.parentId && map[cat.parentId]) {
      map[cat.parentId].children.push(map[cat.id])
    } else {
      roots.push(map[cat.id])
    }
  })
  return roots
})

// 扁平化分类（用于选择父级，排除三级）
const flatCategories = computed(() => {
  return categories.value
    .filter(c => c.level < 3)
    .map(c => ({
      ...c,
      displayName: `${c.level === 1 ? '' : c.level === 2 ? '└ ' : '└ └ '}${c.name}`
    }))
})

const fetchList = async () => {
  try {
    const res = await getCategoryList()
    if (res.data.code === 200) {
      categories.value = res.data.data
    }
  } catch (e) { /* */ }
}

const openAddDialog = () => {
  isEdit.value = false
  form.value = { id: null, name: '', parentId: 0, level: 1, sortOrder: 0, isShow: 1, isHot: 0, image: '' }
  dialogVisible.value = true
}

const openEditDialog = (row) => {
  isEdit.value = true
  form.value = { ...row }
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (!form.value.name) {
    ElMessage.warning('请输入分类名称')
    return
  }
  submitting.value = true
  try {
    const res = isEdit.value
      ? await updateCategory(form.value)
      : await addCategory(form.value)
    if (res.data.code === 200) {
      ElMessage.success(res.data.msg)
      dialogVisible.value = false
      fetchList()
    } else {
      ElMessage.error(res.data.msg)
    }
  } catch (e) {
    ElMessage.error('操作失败')
  } finally {
    submitting.value = false
  }
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(`确定删除分类「${row.name}」吗？`, '提示', { type: 'warning' })
    const res = await deleteCategory(row.id)
    if (res.data.code === 200) {
      ElMessage.success('已删除')
      fetchList()
    } else {
      ElMessage.error(res.data.msg)
    }
  } catch (e) { /* 取消 */ }
}

const toggleShow = async (row) => {
  try {
    const res = await toggleCategoryShow(row.id)
    if (res.data.code === 200) {
      ElMessage.success(res.data.msg)
      fetchList()
    }
  } catch (e) { /* */ }
}

onMounted(fetchList)
</script>

<style scoped>
.admin-page { background: #fff; border-radius: 8px; padding: 20px; }
.page-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.page-head h1 { font-size: 20px; color: #1F2937; }
</style>
