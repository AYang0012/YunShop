<template>
  <div class="goods-list-page">
    <header class="top-bar">
      <router-link to="/" class="logo">云集优选</router-link>
      <el-input v-model="keyword" placeholder="搜索商品" class="search-input" @keyup.enter="doSearch" clearable>
        <template #append><el-button @click="doSearch" :icon="Search">搜索</el-button></template>
      </el-input>
      <router-link to="/cart" class="cart-btn"><el-icon :size="24"><ShoppingCart /></el-icon></router-link>
    </header>
    <div class="main">
      <div class="sort-bar">
        <span :class="{ active: sort === 'default' }" @click="setSort('default')">综合</span>
        <span :class="{ active: sort === 'sales' }" @click="setSort('sales')">
          销量<template v-if="sort === 'sales'">{{ order === 'asc' ? '↑' : '↓' }}</template>
        </span>
        <span :class="{ active: sort === 'price' }" @click="setSort('price')">
          价格<template v-if="sort === 'price'">{{ order === 'asc' ? '↑' : '↓' }}</template>
        </span>
        <span :class="{ active: sort === 'time' }" @click="setSort('time')">
          新品<template v-if="sort === 'time'">{{ order === 'asc' ? '↑' : '↓' }}</template>
        </span>
        <div class="page-size">
          <span v-for="s in [12,24,48]" :key="s" :class="{ active: pageSize === s }" @click="pageSize = s; fetchData()">{{ s }}条/页</span>
        </div>
      </div>
      <div class="goods-grid">
        <div v-for="g in goodsList" :key="g.goodsId" class="g-card" @click="$router.push(`/goods/detail/${g.goodsId}`)">
          <div class="g-thumb"><img :src="g.goodsThumb || `/api/images/goods/${g.goodsId}`" :alt="g.goodsName" class="thumb-img" /></div>
          <p class="g-name">{{ g.goodsName }}</p>
          <div class="g-price"><span class="price">¥{{ g.shopPrice }}</span><span class="sales">已售 {{ g.salesSum }}</span></div>
          <p class="g-time">上架 {{ formatDate(g.addTime) }}</p>
        </div>
      </div>
      <el-empty v-if="!goodsList.length" description="暂无商品" />
      <div class="pagination" v-if="total > 0">
        <el-pagination background layout="prev, pager, next" :total="total" :page-size="pageSize" v-model:current-page="page" @change="fetchData" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getGoodsList } from '@/api/goods'

const route = useRoute()
const goodsList = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(12)
const sort = ref('default')
const order = ref('desc')
const keyword = ref(route.query.keyword || '')

const fetchData = async () => {
  const params = {
    catId: route.query.catId || undefined,
    keyword: keyword.value || undefined,
    sort: sort.value === 'default' ? undefined : sort.value,
    order: sort.value === 'default' ? undefined : order.value,
    page: page.value,
    pageSize: pageSize.value
  }
  try {
    const res = await getGoodsList(params)
    if (res.code === 200) {
      goodsList.value = res.data.list
      total.value = res.data.total
    }
  } catch (e) { /* */ }
}

const setSort = (s) => {
  if (sort.value === s) {
    // 同一排序字段：切换升/降序
    order.value = order.value === 'asc' ? 'desc' : 'asc'
  } else {
    // 切换排序字段：设置默认方向（价格默认升序，其余默认降序）
    sort.value = s
    order.value = (s === 'price') ? 'asc' : 'desc'
  }
  page.value = 1
  fetchData()
}

const formatDate = (time) => {
  if (!time) return ''
  return time.substring(0, 10)  // 截取 YYYY-MM-DD
}

const doSearch = () => { page.value = 1; fetchData() }

onMounted(fetchData)
</script>

<style scoped>
.goods-list-page { background: #FAFAF8; min-height: 100vh; }
.top-bar {
  max-width: 100%;
  margin: 0;
  display: flex;
  align-items: center;
  padding: 0 20px;
  height: 56px;
  gap: 16px;
  background: #F5F6F8;
  border-bottom: 1px solid #E6E8EB;
  border-top: 2px solid #E8734A;
  box-shadow: 0 1px 0 rgba(0,0,0,0.03), 0 2px 8px rgba(0,0,0,0.04);
  position: sticky;
  top: 0;
  z-index: 100;
}
.logo { font-size: 20px; font-weight: 700; color: #1A6B7A; text-decoration: none; white-space: nowrap; transition: opacity 0.25s; }
.logo:hover { opacity: 0.8; }
.search-input { max-width: 500px; }
.cart-btn { color: #1F2937; padding: 6px; }
.main { max-width: 1200px; margin: 0 auto; padding: 0 20px; }
.sort-bar { display: flex; align-items: center; gap: 24px; padding: 12px 16px; background: #fff; border-radius: 8px; margin-bottom: 16px; font-size: 14px; }
.sort-bar span { cursor: pointer; color: #6B7280; transition: color .2s; }
.sort-bar span.active { color: #E8734A; font-weight: 600; }
.page-size { margin-left: auto; display: flex; gap: 12px; font-size: 13px; }
.goods-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }
.g-card { background: #fff; border-radius: 8px; padding: 12px; cursor: pointer; transition: all .2s; }
.g-card:hover { transform: translateY(-4px); box-shadow: 0 8px 24px rgba(0,0,0,.08); }
.g-thumb { width: 100%; padding-bottom: 100%; position: relative; border-radius: 6px; overflow: hidden; }
.thumb-img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.g-name { font-size: 14px; color: #1F2937; margin: 8px 0; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.g-price { display: flex; justify-content: space-between; align-items: center; }
.price { font-size: 18px; font-weight: 700; color: #E8734A; }
.sales { font-size: 12px; color: #9CA3AF; }
.g-time { font-size: 11px; color: #B0B7C3; margin-top: 4px; }
.pagination { display: flex; justify-content: center; padding: 32px 0; }
</style>
