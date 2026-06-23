<template>
  <div class="password-page">
    <div class="page-card">
      <h1 class="page-title">修改密码</h1>
      <p class="page-desc">请使用至少两种字符类型，长度 6–16 位</p>

      <el-form :model="form" label-position="top" class="password-form" @submit.prevent="save">
        <el-form-item label="当前密码">
          <el-input v-model="form.oldPassword" type="password" show-password
            placeholder="输入当前登录密码" size="large" :prefix-icon="Lock" />
        </el-form-item>

        <el-form-item label="新密码">
          <el-input v-model="form.newPassword" type="password" show-password
            placeholder="设定新密码" size="large" :prefix-icon="Key" />
          <div class="strength-bar">
            <span v-for="i in 4" :key="i" class="strength-seg"
              :class="strengthClass(i)" :style="{ transitionDelay: `${i*0.08}s` }"></span>
          </div>
        </el-form-item>

        <el-form-item label="确认新密码">
          <el-input v-model="form.confirmPassword" type="password" show-password
            placeholder="再次输入新密码" size="large" :prefix-icon="Key"
            :class="{ 'is-match': form.confirmPassword && form.newPassword === form.confirmPassword }" />
          <p v-if="form.confirmPassword && form.newPassword !== form.confirmPassword"
            class="mismatch-hint">两次密码不一致</p>
        </el-form-item>

        <el-button type="primary" class="save-btn" native-type="submit"
          :loading="saving" :disabled="!canSubmit">
          更新密码
        </el-button>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { Lock, Key } from '@element-plus/icons-vue'
import { changePassword } from '@/api/user'

const form = reactive({ oldPassword: '', newPassword: '', confirmPassword: '' })
const saving = ref(false)

const hasUpper = (s) => /[A-Z]/.test(s)
const hasLower = (s) => /[a-z]/.test(s)
const hasDigit = (s) => /\d/.test(s)
const hasSymbol = (s) => /[!@#$%^&*(),.?":{}|<>~`[\]\\;'/+=_\-]/.test(s)

const strengthLevel = computed(() => {
  const p = form.newPassword
  if (!p) return 0
  let score = 0
  if (hasUpper(p)) score++
  if (hasLower(p)) score++
  if (hasDigit(p)) score++
  if (hasSymbol(p)) score++
  if (p.length >= 6) score = Math.min(score, 4)
  return Math.min(score + (p.length >= 10 ? 1 : 0), 4)
})

const strengthClass = (i) => {
  const level = strengthLevel.value
  if (level >= i) {
    if (level <= 2) return 'weak'
    if (level === 3) return 'medium'
    return 'strong'
  }
  return ''
}

const canSubmit = computed(() => {
  return form.oldPassword && form.newPassword &&
    form.newPassword === form.confirmPassword &&
    form.newPassword.length >= 6
})

const save = async () => {
  if (form.newPassword !== form.confirmPassword) {
    ElMessage.error('两次新密码不一致')
    return
  }
  if (form.newPassword.length < 6) {
    ElMessage.error('新密码至少 6 位')
    return
  }
  saving.value = true
  try {
    await changePassword({ oldPassword: form.oldPassword, newPassword: form.newPassword })
    ElMessage.success('密码修改成功')
    form.oldPassword = ''
    form.newPassword = ''
    form.confirmPassword = ''
  } catch { /* */ }
  finally { saving.value = false }
}
</script>

<style scoped>
/* ====== Page ====== */
.password-page {
  min-height: calc(100vh - 56px);
  background: linear-gradient(180deg, #F5F4F1 0%, #F0EFEC 100%);
  padding: 40px 20px 80px;
}

.page-card {
  max-width: 440px;
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
.page-desc { font-size: 13px; color: #9CA3AF; margin: 0 0 32px; }

/* ====== Form ====== */
.password-form {
  --el-color-primary: #1A6B7A;
  --el-color-primary-hover: #1F8290;
}

.password-form :deep(.el-form-item__label) {
  font-size: 13px; font-weight: 500; color: #4B5563; padding-bottom: 6px;
}
.password-form :deep(.el-input__wrapper) {
  border-radius: 8px;
  box-shadow: 0 0 0 1px #E5E7EB inset;
  transition: box-shadow 0.25s;
}
.password-form :deep(.el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px #D1D5DB inset;
}
.password-form :deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 2px #1A6B7A inset;
}

/* ====== Strength Bar ====== */
.strength-bar {
  display: flex; gap: 5px; margin-top: 8px; height: 3px;
}
.strength-seg {
  flex: 1; border-radius: 2px;
  background: #E5E7EB;
  transition: background 0.3s;
}
.strength-seg.weak { background: #F59E0B; }
.strength-seg.medium { background: #6366F1; }
.strength-seg.strong { background: #10B981; }

.mismatch-hint { font-size: 12px; color: #EF4444; margin: 4px 0 0; }

/* ====== Button ====== */
.save-btn {
  width: 100%; height: 44px; margin-top: 12px;
  font-size: 15px; font-weight: 500; border-radius: 10px;
  background: linear-gradient(135deg, #1A6B7A 0%, #1F8290 100%);
  border: none;
  transition: all 0.3s cubic-bezier(0.22, 0.61, 0.36, 1);
}
.save-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 16px rgba(26,107,122,0.32);
}
.save-btn:active { transform: translateY(0); }

@media (max-width: 480px) {
  .password-page { padding: 20px 12px 60px; }
  .page-card { padding: 32px 24px; }
}
</style>
