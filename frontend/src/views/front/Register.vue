<template>
  <div class="register-page">
    <div class="register-card">
      <h1 class="title">注册云集优选</h1>
      <p class="subtitle">加入我们，发现品质好物</p>
      <el-form ref="formRef" :model="form" :rules="rules" size="large" @submit.prevent="handleRegister">
        <!-- 头像上传 -->
        <el-form-item class="avatar-form-item">
          <div class="avatar-upload" @click="triggerUpload">
            <el-avatar v-if="avatarPreview" :size="80" :src="avatarPreview" />
            <div v-else class="avatar-placeholder">
              <el-icon :size="32"><Plus /></el-icon>
              <span>上传头像</span>
            </div>
            <input ref="fileInput" type="file" accept=".jpg,.jpeg,.png,.webp" style="display:none" @change="handleFileChange" />
          </div>
          <div class="avatar-tip">支持 jpg、png、webp 格式，不超过 5MB（选填）</div>
        </el-form-item>
        <el-form-item>
          <el-radio-group v-model="form.registerType">
            <el-radio-button value="mobile">手机号注册</el-radio-button>
            <el-radio-button value="email">邮箱注册</el-radio-button>
          </el-radio-group>
        </el-form-item>
        <el-form-item prop="account">
          <el-input v-model="form.account"
            :placeholder="form.registerType === 'email' ? '请输入邮箱' : '请输入手机号'"
            clearable />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="form.password" type="password" placeholder="密码 (6-16位，至少两种字符组合)" show-password />
        </el-form-item>
        <el-form-item prop="confirmPassword">
          <el-input v-model="form.confirmPassword" type="password" placeholder="确认密码" show-password />
        </el-form-item>
        <el-form-item>
          <el-input v-model="form.referrerMobile" placeholder="推荐人手机号（选填）" />
        </el-form-item>
        <el-form-item prop="agreeProtocol">
          <el-checkbox v-model="form.agreeProtocol">
            我已阅读并同意 <a href="javascript:void(0)" style="color:#1A6B7A" @click.stop="showAgreement = true">《用户协议》</a>
          </el-checkbox>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" native-type="submit" :loading="loading" class="submit-btn">
            注 册
          </el-button>
        </el-form-item>
      </el-form>
      <div class="links">
        <router-link to="/login">已有账号？立即登录</router-link>
        <router-link to="/">返回首页</router-link>
      </div>
    </div>

    <!-- 用户协议弹框 -->
    <el-dialog v-model="showAgreement" title="用户协议" width="420px" center>
      <div style="text-align:center; padding:20px 0; font-size:15px; line-height:1.8; color:#333;">
        该项目用于筑基开发与测试技术，感谢您的使用！
      </div>
      <template #footer>
        <el-button type="primary" @click="showAgreement = false">我已知悉</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { register, uploadAvatar, updateProfile } from '@/api/user'

const router = useRouter()
const form = reactive({
  account: '', registerType: 'mobile', password: '', confirmPassword: '',
  referrerMobile: '', agreeProtocol: false, avatar: ''
})
const loading = ref(false)
const fileInput = ref(null)
const avatarPreview = ref('')
const avatarFile = ref(null)
const showAgreement = ref(false)

const rules = {
  account: [{ required: true, message: '请输入手机号或邮箱', trigger: 'blur' }],
  password: [{ required: true, min: 6, max: 16, message: '密码6-16位', trigger: 'blur' }],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    { validator: (rule, value, cb) => value !== form.password ? cb(new Error('两次密码不一致')) : cb() }
  ],
  agreeProtocol: [
    { validator: (rule, value, cb) => value ? cb() : cb(new Error('请先阅读并同意用户协议')) }
  ]
}

// 触发文件选择
const triggerUpload = () => {
  fileInput.value.click()
}

// 处理文件选择
const handleFileChange = (e) => {
  const file = e.target.files[0]
  if (!file) return

  // 验证文件类型
  const allowedTypes = ['image/jpeg', 'image/png', 'image/webp']
  if (!allowedTypes.includes(file.type)) {
    ElMessage.error('仅支持 jpg、png、webp 格式')
    return
  }

  // 验证文件大小
  if (file.size > 5 * 1024 * 1024) {
    ElMessage.error('文件大小不能超过 5MB')
    return
  }

  avatarFile.value = file
  // 预览
  const reader = new FileReader()
  reader.onload = (e) => {
    avatarPreview.value = e.target.result
  }
  reader.readAsDataURL(file)
}

const handleRegister = async () => {
  loading.value = true
  try {
    // 先注册（不含头像）
    const res = await register({
      account: form.account,
      registerType: form.registerType,
      password: form.password,
      confirmPassword: form.confirmPassword,
      referrerMobile: form.referrerMobile,
      agreeProtocol: form.agreeProtocol
    })

    // 注册成功后，如果有头像则上传
    if (avatarFile.value) {
      const uploadRes = await uploadAvatar(avatarFile.value)
      if (uploadRes.code === 200) {
        // 更新用户头像
        await updateProfile({ avatar: uploadRes.data.url })
      }
    }

    ElMessage.success(res.msg || '注册成功')
    router.push('/')
  } catch (e) {
    // 错误由拦截器处理
  } finally { loading.value = false }
}
</script>

<style scoped>
.register-page { display: flex; align-items: center; justify-content: center; min-height: 100vh; background: linear-gradient(160deg, #E8F4F7 0%, #FAFAF8 40%, #F5F0EB 100%); }
.register-card { background: #fff; padding: 36px 40px; border-radius: 12px; box-shadow: 0 4px 32px rgba(0,0,0,.06); width: 420px; }
.title { font-size: 24px; font-weight: 700; color: #1A6B7A; text-align: center; letter-spacing: 2px; }
.subtitle { text-align: center; color: #6B7280; margin: 8px 0 24px; font-size: 14px; }
.submit-btn { width: 100%; }
.links { display: flex; justify-content: space-between; font-size: 13px; margin-top: 8px; }
.links a { color: #6B7280; text-decoration: none; }
.links a:hover { color: #1A6B7A; }

/* 头像上传 */
.avatar-form-item { display: flex; flex-direction: column; align-items: center; margin-bottom: 20px; }
.avatar-upload { cursor: pointer; transition: all 0.3s; }
.avatar-upload:hover { transform: scale(1.05); }
.avatar-placeholder {
  width: 80px; height: 80px; border-radius: 50%;
  background: #F5F7FA; border: 2px dashed #C0C4CC;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  color: #909399; font-size: 12px; gap: 4px;
}
.avatar-placeholder:hover { border-color: #1A6B7A; color: #1A6B7A; }
.avatar-tip { font-size: 12px; color: #909399; margin-top: 8px; }
</style>
