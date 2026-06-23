<template>
  <div class="login-page">
    <div class="login-card">
      <h1 class="title">登录云集优选</h1>
      <p class="subtitle">品质生活，尽在云集</p>
      <el-form ref="formRef" :model="form" :rules="rules" size="large" @submit.prevent="handleLogin">
        <el-form-item prop="username">
          <el-input v-model="form.username" placeholder="手机号/邮箱" clearable>
            <template #prefix><el-icon><User /></el-icon></template>
          </el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="form.password" type="password" placeholder="密码" show-password>
            <template #prefix><el-icon><Lock /></el-icon></template>
          </el-input>
        </el-form-item>
        <el-form-item prop="captcha">
          <div class="captcha-row">
            <el-input v-model="form.captcha" placeholder="验证码" style="width: 60%">
              <template #prefix><el-icon><Key /></el-icon></template>
            </el-input>
            <el-button class="captcha-btn" @click="getCaptchaCode" :loading="captchaLoading">
              {{ captchaText || '获取验证码' }}
            </el-button>
          </div>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" native-type="submit" :loading="loading" class="submit-btn">
            登 录
          </el-button>
        </el-form-item>
      </el-form>
      <div class="links">
        <router-link to="/register">还没有账号？立即注册</router-link>
        <router-link to="/">返回首页</router-link>
      </div>
      <div class="third-party">
        <span class="tp-label">第三方登录</span>
        <div class="tp-icons">
          <span class="tp-icon">支付宝</span>
          <span class="tp-icon">QQ</span>
          <span class="tp-icon">微信</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { login, getCaptcha } from '@/api/user'

const router = useRouter()
const form = ref({ username: '', password: '', captcha: '' })
const loading = ref(false)
const captchaText = ref('')
const captchaLoading = ref(false)

const rules = {
  username: [{ required: true, message: '请输入手机号或邮箱', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
  captcha: [{ required: true, message: '请输入验证码', trigger: 'blur' }]
}

const getCaptchaCode = async () => {
  captchaLoading.value = true
  try {
    const res = await getCaptcha()
    captchaText.value = res.data.captcha
  } finally { captchaLoading.value = false }
}

const handleLogin = async () => {
  loading.value = true
  try {
    const res = await login(form.value)
    ElMessage.success(res.msg || '登录成功')
    router.push('/')
  } catch (e) {
    // 错误由拦截器处理
  } finally { loading.value = false }
}
</script>

<style scoped>
.login-page { display: flex; align-items: center; justify-content: center; min-height: 100vh; background: linear-gradient(160deg, #E8F4F7 0%, #FAFAF8 40%, #F5F0EB 100%); }
.login-card { background: #fff; padding: 40px; border-radius: 12px; box-shadow: 0 4px 32px rgba(0,0,0,.06); width: 400px; }
.title { font-size: 24px; font-weight: 700; color: #1A6B7A; text-align: center; letter-spacing: 2px; }
.subtitle { text-align: center; color: #6B7280; margin: 8px 0 28px; font-size: 14px; }
.captcha-row { display: flex; gap: 12px; width: 100%; }
.captcha-btn { white-space: nowrap; min-width: 110px; }
.submit-btn { width: 100%; }
.links { display: flex; justify-content: space-between; font-size: 13px; margin-top: 16px; }
.links a { color: #6B7280; text-decoration: none; }
.links a:hover { color: #1A6B7A; }
.third-party { text-align: center; margin-top: 24px; padding-top: 20px; border-top: 1px solid #E5E7EB; }
.tp-label { font-size: 12px; color: #9CA3AF; }
.tp-icons { display: flex; gap: 16px; justify-content: center; margin-top: 10px; }
.tp-icon { padding: 6px 16px; border: 1px solid #E5E7EB; border-radius: 20px; font-size: 12px; color: #6B7280; cursor: pointer; }
</style>
