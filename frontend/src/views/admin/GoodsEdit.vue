<template>
  <div class="admin-page">
    <div class="page-head">
      <h1>{{ isEdit ? '编辑商品' : '添加商品' }}</h1>
      <el-button @click="$router.back()">返回</el-button>
    </div>
    <el-form :model="form" label-width="100px" style="max-width: 600px">
      <el-form-item label="商品名称"><el-input v-model="form.goodsName" /></el-form-item>
      <el-form-item label="商品编号"><el-input v-model="form.goodsSn" /></el-form-item>
      <el-form-item label="分类ID"><el-input-number v-model="form.catId" /></el-form-item>
      <el-form-item label="品牌ID"><el-input-number v-model="form.brandId" /></el-form-item>
      <el-form-item label="售价"><el-input-number v-model="form.shopPrice" :precision="2" :step="0.01" /></el-form-item>
      <el-form-item label="原价"><el-input-number v-model="form.marketPrice" :precision="2" :step="0.01" /></el-form-item>
      <el-form-item label="库存"><el-input-number v-model="form.storeCount" /></el-form-item>
      <el-form-item label="关键词"><el-input v-model="form.keywords" /></el-form-item>
      <el-form-item label="是否上架">
        <el-switch v-model="form.isOnSale" :active-value="1" :inactive-value="0" />
      </el-form-item>
      <el-form-item label="是否推荐">
        <el-switch v-model="form.isRecommend" :active-value="1" :inactive-value="0" />
      </el-form-item>
      <el-form-item label="详情"><el-input v-model="form.goodsContent" type="textarea" :rows="6" /></el-form-item>
      <el-form-item><el-button type="primary" @click="save">保存</el-button></el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const isEdit = ref(!!route.params.id)
const form = reactive({
  goodsName: '', goodsSn: '', catId: 0, brandId: 0, shopPrice: 0, marketPrice: 0,
  storeCount: 0, keywords: '', isOnSale: 1, isRecommend: 0, goodsContent: ''
})

onMounted(async () => {
  if (isEdit.value) {
    try {
      const res = await axios.get(`/api/goods/detail/${route.params.id}`)
      if (res.data.code === 200) Object.assign(form, res.data.data.goods)
    } catch (e) { /* */ }
  }
})

const save = async () => {
  try {
    const url = isEdit.value ? `/api/admin/goods/update` : `/api/admin/goods/add`
    const method = isEdit.value ? 'put' : 'post'
    await axios[method](url, { ...form })
    ElMessage.success('保存成功'); router.back()
  } catch (e) { /* */ }
}
</script>

<style scoped>
.admin-page { background: #fff; border-radius: 8px; padding: 20px; }
.page-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.page-head h1 { font-size: 20px; color: #1F2937; }
</style>
