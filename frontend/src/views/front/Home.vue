<template>
  <div class="home">
    <!-- 顶部导航栏 -->
    <Header />

    <!-- 分类菜单 + Banner -->
    <section class="hero">
      <div class="hero-inner">
        <!-- 左侧分类菜单 -->
        <div class="category-menu" @mouseleave="activeCat = null">
          <div v-for="cat in categories" :key="cat.category.id"
            class="cat-item" :class="{ active: activeCat === cat.category.id }"
            @mouseenter="activeCat = cat.category.id"
            @click="goCategory(cat.category.id)">
            <span class="cat-indicator"></span>
            <span class="cat-name">{{ cat.category.name }}</span>
            <el-icon class="cat-arrow"><ArrowRight /></el-icon>
          </div>
        </div>
        <!-- 分类弹出层 -->
        <div v-if="activeCat" class="category-popup" @mouseleave="activeCat = null">
          <div v-for="cat in activeCatChildren" :key="cat.category.id" class="popup-col">
            <router-link :to="`/goods/list?catId=${cat.category.id}`" class="popup-title">
              {{ cat.category.name }}
            </router-link>
            <div class="popup-tags">
              <router-link v-for="child in cat.children" :key="child.id"
                :to="`/goods/list?catId=${child.id}`" class="popup-tag">
                {{ child.name }}
              </router-link>
            </div>
          </div>
        </div>
        <!-- Banner 轮播 -->
        <div class="banner" @mouseenter="pauseBanner = true" @mouseleave="pauseBanner = false">
          <div v-if="banners.length > 1" class="carousel-wrapper">
            <div class="carousel-track" :style="{ transform: `translateX(-${currentSlide * 100}%)` }">
              <div v-for="b in banners" :key="b.adId" class="carousel-slide">
                <a :href="b.adLink || '#'" class="banner-link">
                  <img :src="b.adImage || `/api/images/banner/${b.adId}`" :alt="b.adName" class="banner-img" />
                </a>
              </div>
            </div>
            <!-- 左右箭头 -->
            <button class="carousel-arrow left" @click="prevSlide">&lt;</button>
            <button class="carousel-arrow right" @click="nextSlide">&gt;</button>
            <!-- 指示器圆点 -->
            <div class="carousel-dots">
              <span v-for="(b, idx) in banners" :key="b.adId"
                class="carousel-dot" :class="{ active: idx === currentSlide }"
                @click="goSlide(idx)"></span>
            </div>
          </div>
          <div v-else-if="banners.length === 1" class="banner-single">
            <a :href="banners[0].adLink || '#'" class="banner-link">
              <img :src="banners[0].adImage || `/api/images/banner/${banners[0].adId}`" :alt="banners[0].adName" class="banner-img" />
            </a>
          </div>
          <div v-else class="banner-empty">品质生活，尽在云集</div>
        </div>
      </div>
    </section>

    <!-- 商品楼层 -->
    <section v-for="floor in floors" :key="floor.category.id" class="floor">
      <div class="floor-header">
        <h2 class="floor-title">{{ floor.category.name }}</h2>
        <div class="floor-subs">
          <router-link v-for="sub in floor.subCategories" :key="sub.id"
            :to="`/goods/list?catId=${sub.id}`" class="floor-sub">{{ sub.name }}</router-link>
        </div>
        <router-link :to="`/goods/list?catId=${floor.category.id}`" class="floor-more">更多 ›</router-link>
      </div>
      <div class="floor-goods">
        <div v-for="goods in floor.goodsList" :key="goods.goodsId" class="goods-card"
          @click="$router.push(`/goods/detail/${goods.goodsId}`)">
          <div class="goods-thumb">
            <img :src="goods.goodsThumb || `/api/images/goods/${goods.goodsId}`" :alt="goods.goodsName" class="thumb-img" />
          </div>
          <p class="goods-name">{{ goods.goodsName }}</p>
          <div class="goods-price">
            <span class="price-current">¥{{ goods.shopPrice }}</span>
            <span class="price-old" v-if="goods.marketPrice > goods.shopPrice">¥{{ goods.marketPrice }}</span>
          </div>
        </div>
      </div>
    </section>

    <!-- 热门推荐 -->
    <section class="hot-section">
      <h2 class="section-title">热门推荐</h2>
      <div class="hot-grid">
        <div v-for="goods in hotGoods" :key="goods.goodsId" class="goods-card"
          @click="$router.push(`/goods/detail/${goods.goodsId}`)">
          <div class="goods-thumb">
            <img :src="goods.goodsThumb || `/api/images/goods/${goods.goodsId}`" :alt="goods.goodsName" class="thumb-img" />
          </div>
          <p class="goods-name">{{ goods.goodsName }}</p>
          <div class="goods-price">
            <span class="price-current">¥{{ goods.shopPrice }}</span>
          </div>
        </div>
      </div>
    </section>

    <!-- 底部 -->
    <footer class="footer">
      <p>© 2026 云集优选 — 品质生活，尽在云集</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import Header from '@/components/Header.vue'
import { getHomeData } from '@/api/goods'

const router = useRouter()

const categories = ref([])
const banners = ref([])
const floors = ref([])
const hotGoods = ref([])
const activeCat = ref(null)
const pauseBanner = ref(false)

// 轮播图状态
const currentSlide = ref(0)
let autoTimer = null

const activeCatChildren = computed(() => {
  if (!activeCat.value) return []
  const cat = categories.value.find(c => c.category.id === activeCat.value)
  return cat ? cat.children : []
})

// 分类菜单点击跳转
const goCategory = (catId) => {
  router.push(`/goods/list?catId=${catId}`)
}

// 轮播图切换
const goSlide = (idx) => {
  currentSlide.value = idx
  resetAutoPlay()
}

const prevSlide = () => {
  currentSlide.value = currentSlide.value === 0 ? banners.value.length - 1 : currentSlide.value - 1
  resetAutoPlay()
}

const nextSlide = () => {
  currentSlide.value = currentSlide.value === banners.value.length - 1 ? 0 : currentSlide.value + 1
  resetAutoPlay()
}

const startAutoPlay = () => {
  stopAutoPlay()
  if (banners.value.length <= 1) return
  autoTimer = setInterval(() => {
    if (!pauseBanner.value) {
      nextSlide()
    }
  }, 3000)
}

const stopAutoPlay = () => {
  if (autoTimer) {
    clearInterval(autoTimer)
    autoTimer = null
  }
}

const resetAutoPlay = () => {
  stopAutoPlay()
  startAutoPlay()
}

// 监听 banners 加载后启动自动播放
watch(banners, (val) => {
  if (val && val.length > 1) {
    startAutoPlay()
  }
})

onMounted(async () => {
  try {
    const res = await getHomeData()
    if (res.code === 200) {
      const d = res.data
      categories.value = d.categoryMenu || []
      banners.value = d.bannerList || []
      floors.value = d.floors || []
      hotGoods.value = d.hotGoods || []
    }
  } catch (e) { /* 使用默认空值 */ }
})

onUnmounted(() => {
  stopAutoPlay()
})
</script>

<style scoped>
/* ====== 变量 ====== */
:root {
  --primary: #1A6B7A;
  --primary-light: #E8F4F7;
  --accent: #E8734A;
  --bg: #FAFAF8;
  --surface: #FFFFFF;
  --text: #1F2937;
  --text-secondary: #6B7280;
  --border: #E5E7EB;
}

.home { background: var(--bg); min-height: 100vh; }

/* ====== Hero ====== */
.hero { background: var(--surface); }
.hero-inner { max-width: 1200px; margin: 0 auto; display: flex; position: relative; height: 420px; }
/* ====== 分类菜单 ====== */
.category-menu {
  width: 220px;
  background: linear-gradient(180deg, #F8F9FA 0%, #F5F6F8 100%);
  padding: 8px 0;
  flex-shrink: 0;
  border-right: 1px solid #EDEFF2;
}

.cat-item {
  display: flex;
  align-items: center;
  padding: 11px 16px 11px 0;
  cursor: pointer;
  font-size: 14px;
  color: var(--text);
  position: relative;
  transition: background 0.3s ease;
  overflow: hidden;
}

/* 左侧指示条 — 默认隐藏 */
.cat-indicator {
  position: absolute;
  left: 0;
  top: 8px;
  bottom: 8px;
  width: 3px;
  background: var(--accent);
  border-radius: 0 2px 2px 0;
  transform: scaleY(0);
  transition: transform 0.3s cubic-bezier(0.25, 0.8, 0.25, 1.2);
}

/* hover / active 时指示条展开 */
.cat-item:hover .cat-indicator,
.cat-item.active .cat-indicator {
  transform: scaleY(1);
}

/* 背景 — hover 时浅青从左滑入 */
.cat-item::before {
  content: '';
  position: absolute;
  inset: 2px 4px;
  background: linear-gradient(90deg, #E8F4F7 0%, #F0F7F9 100%);
  border-radius: 6px;
  opacity: 0;
  transition: opacity 0.3s ease;
  z-index: 0;
}
.cat-item:hover::before,
.cat-item.active::before {
  opacity: 1;
}

/* 文字 */
.cat-name {
  position: relative;
  z-index: 1;
  margin-left: 16px;
  transition: transform 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  white-space: nowrap;
}
.cat-item:hover .cat-name,
.cat-item.active .cat-name {
  transform: translateX(4px);
  color: var(--primary);
  font-weight: 500;
}

/* 箭头图标 */
.cat-arrow {
  position: relative;
  z-index: 1;
  margin-left: auto;
  margin-right: 8px;
  font-size: 13px;
  opacity: 0.4;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}
.cat-item:hover .cat-arrow,
.cat-item.active .cat-arrow {
  opacity: 1;
  transform: translateX(3px);
  color: var(--accent);
}

/* ====== 弹出层 ====== */
.category-popup {
  position: absolute;
  left: 220px;
  top: 0;
  width: 580px;
  background: rgba(255, 255, 255, 0.94);
  backdrop-filter: blur(16px) saturate(180%);
  -webkit-backdrop-filter: blur(16px) saturate(180%);
  box-shadow:
    8px 8px 32px rgba(0, 0, 0, 0.06),
    0 0 0 1px rgba(0, 0, 0, 0.04);
  z-index: 50;
  display: flex;
  padding: 24px 28px;
  min-height: 420px;
  border-radius: 0 12px 12px 0;
  animation: popupIn 0.25s cubic-bezier(0.25, 0.8, 0.25, 1);
}
@keyframes popupIn {
  from { opacity: 0; transform: translateX(-8px); }
  to   { opacity: 1; transform: translateX(0); }
}

.popup-col {
  flex: 1;
  padding-right: 12px;
}
.popup-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text);
  text-decoration: none;
  display: block;
  margin-bottom: 10px;
  padding-bottom: 8px;
  border-bottom: 2px solid transparent;
  transition: all 0.25s;
}
.popup-title:hover {
  color: var(--primary);
  border-bottom-color: var(--primary-light);
}

.popup-tags { display: flex; flex-wrap: wrap; gap: 6px; }

.popup-tag {
  font-size: 12px;
  color: var(--text-secondary);
  text-decoration: none;
  padding: 3px 10px;
  background: #F5F6F8;
  border-radius: 4px;
  transition: all 0.25s cubic-bezier(0.25, 0.8, 0.25, 1);
  border: 1px solid transparent;
}
.popup-tag:hover {
  color: var(--accent);
  background: #FFF5F0;
  border-color: #FDE0D4;
  transform: scale(1.06);
}

/* ====== Banner 轮播 ====== */
.banner { flex: 1; overflow: hidden; position: relative; }
.banner-link { display: flex; align-items: center; justify-content: center; height: 100%; text-decoration: none; }
.banner-img { width: 100%; height: 100%; object-fit: cover; }

.carousel-wrapper { position: relative; width: 100%; height: 420px; overflow: hidden; }
.carousel-track { display: flex; height: 100%; transition: transform 0.5s cubic-bezier(0.25, 0.8, 0.25, 1); }
.carousel-slide { flex: 0 0 100%; height: 100%; }

/* 左右箭头 */
.carousel-arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  z-index: 10;
  width: 40px; height: 60px;
  background: rgba(0,0,0,0.3);
  color: #fff;
  border: none;
  font-size: 20px;
  cursor: pointer;
  opacity: 0;
  transition: opacity 0.3s;
}
.carousel-wrapper:hover .carousel-arrow { opacity: 1; }
.carousel-arrow.left { left: 0; border-radius: 0 4px 4px 0; }
.carousel-arrow.right { right: 0; border-radius: 4px 0 0 4px; }
.carousel-arrow:hover { background: rgba(0,0,0,0.55); }

/* 指示器圆点 */
.carousel-dots {
  position: absolute;
  bottom: 16px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 10px;
  z-index: 10;
}
.carousel-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: rgba(255,255,255,0.5);
  border: 2px solid rgba(255,255,255,0.8);
  cursor: pointer;
  transition: all 0.3s;
}
.carousel-dot.active {
  background: #E8734A;
  border-color: #E8734A;
  transform: scale(1.15);
}
.carousel-dot:hover {
  background: rgba(255,255,255,0.9);
  border-color: #fff;
}

.banner-single { height: 420px; }
.banner-single .banner-img { width: 100%; height: 100%; object-fit: cover; }
.banner-empty { height: 420px; display: flex; align-items: center; justify-content: center; font-size: 32px; color: var(--primary); background: linear-gradient(135deg, var(--primary-light), #F5F0EB); }

/* ====== Floor ====== */
.floor { max-width: 1200px; margin: 24px auto 0; background: var(--surface); border-radius: 8px; padding: 24px; }
.floor-header { display: flex; align-items: center; margin-bottom: 16px; }
.floor-title { font-size: 20px; font-weight: 700; color: var(--text); margin-right: 20px; }
.floor-subs { display: flex; gap: 16px; flex: 1; }
.floor-sub { font-size: 13px; color: var(--text-secondary); text-decoration: none; transition: color .2s; }
.floor-sub:hover { color: var(--accent); }
.floor-more { font-size: 13px; color: var(--text-secondary); text-decoration: none; }
.floor-more:hover { color: var(--primary); }
.floor-goods { display: grid; grid-template-columns: repeat(6, 1fr); gap: 16px; }

/* ====== Goods Card ====== */
.goods-card { cursor: pointer; transition: transform .2s, box-shadow .2s; border-radius: 8px; padding: 8px; }
.goods-card:hover { transform: translateY(-4px); box-shadow: 0 8px 24px rgba(0,0,0,.08); }
.goods-thumb { width: 100%; padding-bottom: 100%; position: relative; overflow: hidden; border-radius: 6px; background: var(--bg); }
.thumb-img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.goods-name { font-size: 13px; color: var(--text); margin: 8px 0 4px; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; line-height: 1.5; }
.goods-price { display: flex; align-items: baseline; gap: 6px; }
.price-current { font-size: 16px; font-weight: 700; color: var(--accent); }
.price-old { font-size: 12px; color: var(--text-secondary); text-decoration: line-through; }

/* ====== Hot ====== */
.hot-section { max-width: 1200px; margin: 24px auto; background: var(--surface); border-radius: 8px; padding: 24px; }
.section-title { font-size: 20px; font-weight: 700; color: var(--text); margin-bottom: 16px; }
.hot-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }

/* ====== Footer ====== */
.footer { text-align: center; padding: 32px 0; color: var(--text-secondary); font-size: 13px; border-top: 1px solid var(--border); margin-top: 40px; }
</style>
