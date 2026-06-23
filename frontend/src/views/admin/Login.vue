<template>
  <div class="admin-login">
    <div class="login-card">
      <h1>云集优选 · 后台管理</h1>
      <el-form :model="form" size="large" @submit.prevent="handleLogin">
        <el-form-item><el-input v-model="form.username" placeholder="管理员用户名" /></el-form-item>
        <el-form-item><el-input v-model="form.password" type="password" placeholder="密码" show-password /></el-form-item>
        <el-form-item><el-button type="primary" native-type="submit" :loading="loading" class="submit-btn">登 录</el-button></el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const router = useRouter()
const form = ref({ username: '', password: '' })
const loading = ref(false)

const handleLogin = async () => {
  loading.value = true
  try {
    const res = await axios.post('/api/admin/login', form.value)
    if (res.data.code === 200) {
      ElMessage.success('登录成功')
      router.push('/admin')
    } else {
      ElMessage.error(res.data.msg)
    }
  } catch (e) { ElMessage.error('登录失败') }
  finally { loading.value = false }
}
</script>

<style scoped>
.admin-login { display: flex; align-items: center; justify-content: center; min-height: 100vh; background: #1F2937; }
.login-card { background: #fff; padding: 48px 40px; border-radius: 12px; width: 400px; }
.login-card h1 { text-align: center; font-size: 22px; color: #1F2937; margin-bottom: 32px; }
.submit-btn { width: 100%; }
</style>
