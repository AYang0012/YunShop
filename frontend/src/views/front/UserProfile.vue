<template>
  <div class="profile-page">
    <div class="profile-card">
      <!-- 页面标题 -->
      <h1 class="page-title">个人信息</h1>
      <p class="page-desc">管理您的账户资料与头像</p>

      <!-- 头像区 -->
      <div class="avatar-zone">
        <div class="avatar-wrapper" @click="triggerUpload" title="点击更换头像">
          <img v-if="avatarPreview" :src="avatarPreview" class="avatar-img" alt="头像" />
          <span v-else class="avatar-placeholder">{{ initial }}</span>
          <div class="avatar-overlay">
            <el-icon :size="22"><Camera /></el-icon>
            <span>{{ avatarPreview ? '更换' : '上传' }}</span>
          </div>
        </div>
        <input ref="fileInput" type="file" accept=".png,.jpg,.jpeg" class="file-input-hidden"
          @change="onFileChange" />
        <p v-if="uploading" class="avatar-hint uploading">正在上传...</p>
        <p v-else-if="avatarPreview" class="avatar-hint clickable" @click="triggerUpload">点击头像更换图片</p>
        <p v-else class="avatar-hint">点击上传 .png 或 .jpg 头像</p>
      </div>

      <!-- 表单区 -->
      <el-form :model="form" label-position="top" class="profile-form" @submit.prevent>
        <el-form-item label="昵称">
          <el-input v-model="form.nickname" placeholder="给自己取一个名字"
            maxlength="20" show-word-limit :prefix-icon="UserFilled" size="large" />
        </el-form-item>

        <el-form-item label="手机号">
          <el-input :model-value="form.mobile || '未绑定'" disabled size="large" />
        </el-form-item>

        <el-button type="primary" class="save-btn" @click="save"
          :loading="saving" :disabled="!form.nickname">
          保存修改
        </el-button>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Camera, UserFilled } from '@element-plus/icons-vue'
import { getCurrentUser, updateProfile, uploadAvatar } from '@/api/user'

const fileInput = ref(null)
const avatarFile = ref(null)
const avatarPreview = ref('')
const uploading = ref(false)
const saving = ref(false)

const form = reactive({ nickname: '', avatar: '', mobile: '' })

const initial = computed(() => {
  return form.nickname ? form.nickname.charAt(0).toUpperCase() : '?'
})

const triggerUpload = () => {
  fileInput.value?.click()
}

const onFileChange = async (e) => {
  const file = e.target.files?.[0]
  if (!file) return

  // 本地预览
  const reader = new FileReader()
  reader.onload = (ev) => { avatarPreview.value = ev.target.result }
  reader.readAsDataURL(file)

  // 上传
  uploading.value = true
  try {
    const res = await uploadAvatar(file)
    if (res.code === 200) {
      form.avatar = res.data.url
      ElMessage.success('头像上传成功')
    } else {
      ElMessage.error(res.msg || '上传失败')
      avatarPreview.value = form.avatar || ''
    }
  } catch {
    ElMessage.error('上传失败，请重试')
    avatarPreview.value = form.avatar || ''
  } finally {
    uploading.value = false
    if (fileInput.value) fileInput.value.value = ''
  }
}

const save = async () => {
  if (!form.nickname.trim()) {
    ElMessage.warning('请输入昵称')
    return
  }
  saving.value = true
  try {
    await updateProfile({ nickname: form.nickname, avatar: form.avatar })
    ElMessage.success('保存成功')
  } catch {
    ElMessage.error('保存失败')
  } finally {
    saving.value = false
  }
}

onMounted(async () => {
  try {
    const r = await getCurrentUser()
    if (r.code === 200) {
      const d = r.data
      form.nickname = d.nickname || ''
      form.avatar = d.avatar || ''
      form.mobile = d.mobile || ''
      if (form.avatar) avatarPreview.value = form.avatar
    }
  } catch { /* */ }
})
</script>

<style scoped>
/* ====== 页面底色 ====== */
.profile-page {
  min-height: 100vh;
  background: linear-gradient(180deg, #F5F4F1 0%, #F0EFEC 100%);
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding: 64px 20px 80px;
}

/* ====== 卡片 ====== */
.profile-card {
  width: 100%;
  max-width: 440px;
  background: #FFFFFF;
  border-radius: 16px;
  padding: 48px 40px 40px;
  box-shadow:
    0 1px 0 rgba(0,0,0,0.04),
    0 4px 24px rgba(0,0,0,0.05),
    0 16px 64px rgba(0,0,0,0.03);
  animation: cardIn 0.5s cubic-bezier(0.22, 0.61, 0.36, 1);
}

@keyframes cardIn {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* ====== 标题 ====== */
.page-title {
  font-family: Georgia, 'Times New Roman', serif;
  font-size: 26px;
  font-weight: 400;
  color: #1F2937;
  margin: 0 0 4px;
  letter-spacing: 0.5px;
}
.page-desc {
  font-size: 13px;
  color: #9CA3AF;
  margin: 0 0 36px;
}

/* ====== 头像区 ====== */
.avatar-zone {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 32px;
}

.avatar-wrapper {
  position: relative;
  width: 96px;
  height: 96px;
  border-radius: 50%;
  cursor: pointer;
  overflow: hidden;
  background: linear-gradient(135deg, #E8F4F7 0%, #F0F4F8 100%);
  box-shadow: 0 0 0 4px #FFFFFF, 0 0 0 5px #E5E7EB;
  transition: box-shadow 0.35s cubic-bezier(0.22, 0.61, 0.36, 1);
  flex-shrink: 0;
}

.avatar-wrapper:hover {
  box-shadow:
    0 0 0 4px #FFFFFF,
    0 0 0 5px #1A6B7A,
    0 0 24px rgba(26,107,122,0.18);
}

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: filter 0.35s;
}
.avatar-wrapper:hover .avatar-img {
  filter: brightness(0.75);
}

.avatar-placeholder {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 36px;
  font-weight: 600;
  color: #1A6B7A;
  font-family: Georgia, 'Times New Roman', serif;
  transition: opacity 0.35s;
  user-select: none;
}

/* 悬停叠加层 */
.avatar-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  background: rgba(26,107,122,0.55);
  color: #fff;
  font-size: 12px;
  opacity: 0;
  transition: opacity 0.35s cubic-bezier(0.22, 0.61, 0.36, 1);
}
.avatar-wrapper:hover .avatar-overlay {
  opacity: 1;
}

.file-input-hidden {
  display: none;
}

.avatar-hint {
  margin-top: 12px;
  font-size: 12px;
  color: #9CA3AF;
  user-select: none;
}
.avatar-hint.clickable {
  color: #1A6B7A;
  cursor: pointer;
  transition: color 0.2s;
}
.avatar-hint.clickable:hover { color: #E8734A; }
.avatar-hint.uploading { color: #E8734A; }

/* ====== 表单 ====== */
.profile-form {
  --el-color-primary: #1A6B7A;
  --el-color-primary-hover: #1F8290;
}

.profile-form :deep(.el-form-item__label) {
  font-size: 13px;
  font-weight: 500;
  color: #4B5563;
  padding-bottom: 6px;
}

.profile-form :deep(.el-input__wrapper) {
  border-radius: 8px;
  box-shadow: 0 0 0 1px #E5E7EB inset;
  transition: box-shadow 0.25s;
}
.profile-form :deep(.el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px #D1D5DB inset;
}
.profile-form :deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 2px #1A6B7A inset;
}

/* ====== 保存按钮 ====== */
.save-btn {
  width: 100%;
  height: 44px;
  margin-top: 8px;
  font-size: 15px;
  font-weight: 500;
  border-radius: 10px;
  background: linear-gradient(135deg, #1A6B7A 0%, #1F8290 100%);
  border: none;
  transition: all 0.3s cubic-bezier(0.22, 0.61, 0.36, 1);
}
.save-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 16px rgba(26,107,122,0.32);
}
.save-btn:active {
  transform: translateY(0);
}

/* ====== 响应式 ====== */
@media (max-width: 480px) {
  .profile-page { padding: 24px 16px 60px; }
  .profile-card { padding: 32px 24px 28px; }
}
</style>
