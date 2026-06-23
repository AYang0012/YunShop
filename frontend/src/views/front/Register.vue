<template>
  <div class="register-page">
    <div class="register-card">
      <h1 class="title">注册云集优选</h1>
      <p class="subtitle">加入我们，发现品质好物</p>
      <el-form ref="formRef" :model="form" :rules="rules" size="large" @submit.prevent="handleRegister">
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
            我已阅读并同意 <a href="#" style="color:#1A6B7A">《用户协议》</a>
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
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { register } from '@/api/user'

const router = useRouter()
const form = reactive({
  account: '', registerType: 'mobile', password: '', confirmPassword: '',
  referrerMobile: '', agreeProtocol: false
})
const loading = ref(false)

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

const handleRegister = async () => {
  loading.value = true
  try {
    const res = await register({ ...form })
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
</style>
