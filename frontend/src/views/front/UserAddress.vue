<template>
  <div class="address-page">
    <div class="page-card">
      <div class="page-header">
        <div>
          <h1 class="page-title">收货地址</h1>
          <p class="page-desc">管理您的配送地址，最多 20 个</p>
        </div>
        <el-button class="add-btn" @click="openDialog()">
          <el-icon :size="16"><Plus /></el-icon>新增地址
        </el-button>
      </div>

      <!-- 地址列表 -->
      <div v-if="addresses.length" class="addr-list">
        <div v-for="(addr, idx) in addresses" :key="addr.addressId"
          class="addr-card" :class="{ 'addr-default': addr.isDefault === 1 }"
          :style="{ animationDelay: `${idx * 0.06}s` }">
          <div v-if="addr.isDefault === 1" class="default-badge">默认</div>
          <div class="addr-body">
            <div class="addr-contact">
              <span class="addr-name">{{ addr.consignee }}</span>
              <span class="addr-phone">{{ addr.mobile }}</span>
            </div>
            <p class="addr-full">
              {{ addr.province }}{{ addr.city }}{{ addr.district }} {{ addr.address }}
            </p>
          </div>
          <div class="addr-actions">
            <el-button text size="small" @click="openDialog(addr)">编辑</el-button>
            <el-button text size="small" type="danger" @click="doDelete(addr.addressId)">删除</el-button>
            <el-button v-if="addr.isDefault !== 1" text size="small" @click="doSetDefault(addr.addressId)">设为默认</el-button>
          </div>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-else class="empty-state">
        <el-icon :size="48" color="#D1D5DB"><MapLocation /></el-icon>
        <p>暂无收货地址</p>
        <el-button class="first-addr-btn" @click="openDialog()">添加第一个地址</el-button>
      </div>
    </div>

    <!-- 新增/编辑弹窗 -->
    <el-dialog v-model="dialogVisible" :title="editingId ? '编辑地址' : '新增地址'" width="460px" destroy-on-close>
      <el-form :model="form" label-position="top">
        <el-row :gutter="12">
          <el-col :span="12">
            <el-form-item label="收货人">
              <el-input v-model="form.consignee" placeholder="姓名" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="手机号">
              <el-input v-model="form.mobile" placeholder="11位手机号" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="12">
          <el-col :span="8">
            <el-form-item label="省份"><el-input v-model="form.province" /></el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="城市"><el-input v-model="form.city" /></el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="区/县"><el-input v-model="form.district" /></el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="详细地址">
          <el-input v-model="form.address" type="textarea" :rows="2" placeholder="街道、楼栋、门牌号" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveAddress" :disabled="!form.consignee || !form.mobile">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, MapLocation } from '@element-plus/icons-vue'
import { getAddressList, addAddress, updateAddress, deleteAddress, setDefaultAddress } from '@/api/address'

const addresses = ref([])
const dialogVisible = ref(false)
const editingId = ref(null)
const form = reactive({ consignee: '', mobile: '', province: '', city: '', district: '', address: '' })

const fetchList = async () => {
  try { const r = await getAddressList(); if (r.code === 200) addresses.value = r.data } catch { /* */ }
}

const openDialog = (addr) => {
  if (addr) {
    editingId.value = addr.addressId
    Object.assign(form, addr)
  } else {
    editingId.value = null
    Object.assign(form, { consignee: '', mobile: '', province: '', city: '', district: '', address: '' })
  }
  dialogVisible.value = true
}

const saveAddress = async () => {
  try {
    if (editingId.value) {
      await updateAddress({ ...form, addressId: editingId.value })
    } else {
      await addAddress({ ...form })
    }
    ElMessage.success('保存成功'); dialogVisible.value = false; fetchList()
  } catch { /* */ }
}

const doDelete = async (id) => {
  try {
    await ElMessageBox.confirm('确定删除该地址吗？', '提示', { type: 'warning' })
    await deleteAddress(id); ElMessage.success('已删除'); fetchList()
  } catch { /* */ }
}

const doSetDefault = async (id) => {
  await setDefaultAddress(id); ElMessage.success('已设为默认'); fetchList()
}

onMounted(fetchList)
</script>

<style scoped>
/* ====== Page ====== */
.address-page {
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

.page-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 28px; }
.page-title {
  font-family: Georgia, 'Times New Roman', serif;
  font-size: 26px; font-weight: 400; color: #1F2937;
  margin: 0 0 4px; letter-spacing: 0.5px;
}
.page-desc { font-size: 13px; color: #9CA3AF; margin: 0; }

.add-btn {
  height: 40px; border-radius: 10px; font-weight: 500;
  background: linear-gradient(135deg, #1A6B7A 0%, #1F8290 100%);
  border: none; color: #fff;
  transition: all 0.3s;
}
.add-btn:hover { transform: translateY(-1px); box-shadow: 0 4px 16px rgba(26,107,122,0.32); color: #fff; }

/* ====== Address Card ====== */
.addr-list { display: flex; flex-direction: column; gap: 10px; }
.addr-card {
  position: relative;
  padding: 18px 20px;
  border: 1px solid #EAEAE8; border-radius: 12px;
  transition: all 0.25s cubic-bezier(0.22, 0.61, 0.36, 1);
  animation: fadeSlide 0.4s cubic-bezier(0.22, 0.61, 0.36, 1) both;
}
@keyframes fadeSlide {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}
.addr-card:hover { border-color: #D1D5DB; box-shadow: 0 2px 12px rgba(0,0,0,0.04); }
.addr-card.addr-default { border-color: #1A6B7A; background: #FAFCFC; }

.default-badge {
  position: absolute; top: 0; right: 16px;
  background: #1A6B7A; color: #fff;
  font-size: 11px; padding: 2px 10px 3px;
  border-radius: 0 0 6px 6px; letter-spacing: 0.5px;
}

.addr-body { margin-bottom: 12px; }
.addr-contact { display: flex; align-items: baseline; gap: 12px; margin-bottom: 6px; }
.addr-name { font-size: 15px; font-weight: 600; color: #1F2937; }
.addr-phone { font-size: 13px; color: #6B7280; }
.addr-full { font-size: 13px; color: #6B7280; line-height: 1.6; margin: 0; }

.addr-actions { display: flex; gap: 4px; }

/* ====== Empty ====== */
.empty-state { text-align: center; padding: 48px 0; }
.empty-state p { color: #9CA3AF; margin: 12px 0 16px; font-size: 14px; }
.first-addr-btn { border-radius: 10px; }

@media (max-width: 480px) {
  .address-page { padding: 20px 12px 60px; }
  .page-card { padding: 24px 18px; }
  .page-header { flex-direction: column; gap: 12px; }
}
</style>
