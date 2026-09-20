import { computed, createApp, onMounted, ref } from 'vue'
import './style.css'
import { router, navigate } from './router.js'

const api = async (path, options = {}) => {
  const response = await fetch(`/api${path}`, { headers: { 'Content-Type': 'application/json' }, ...options })
  const payload = await response.json()
  if (!response.ok) throw new Error(payload.detail || 'عملیات ناموفق بود.')
  return payload
}

const App = {
  setup() {
    const activeView = ref(router.current().id)
    const health = ref(null)
    const dashboard = ref(null)
    const products = ref([])
    const error = ref('')
    const notice = ref('')
    const loading = ref(false)
    const product = ref({ name: '', barcode: '', retail_price: 0, min_stock: 0 })
    const nav = router.routes

    const title = computed(() => nav.find(item => item.id === activeView.value)?.label || '')
    const money = value => new Intl.NumberFormat('fa-IR').format(Number(value || 0))
    const loadProducts = async () => { products.value = await api('/products') }
    const loadDashboard = async () => { dashboard.value = await api('/dashboard') }
    const refresh = async () => {
      loading.value = true; error.value = ''
      try { health.value = await api('/health'); await Promise.all([loadDashboard(), loadProducts()]) }
      catch (err) { error.value = err.message }
      finally { loading.value = false }
    }
    const addProduct = async () => {
      notice.value = ''; error.value = ''
      try {
        await api('/products', { method: 'POST', body: JSON.stringify(product.value) })
        product.value = { name: '', barcode: '', retail_price: 0, min_stock: 0 }
        notice.value = 'کالا با موفقیت ثبت شد.'
        await Promise.all([loadProducts(), loadDashboard()])
      } catch (err) { error.value = err.message }
    }
    onMounted(() => {
      const syncRoute = () => { activeView.value = router.current().id }
      window.addEventListener('route-change', syncRoute)
      window.addEventListener('popstate', syncRoute)
      syncRoute()
      refresh()
    })
    return { activeView, health, dashboard, products, error, notice, loading, product, nav, title, money, refresh, addProduct }
  },
  template: `
    <div class="app-shell">
      <aside class="sidebar"><div class="brand"><span>LC</span><strong>هسته بازرگانی</strong><small>محلی و آفلاین</small></div>
        <nav><button v-for="item in nav" :key="item.id" :class="{active: activeView === item.id}" @click="navigate(item.path)">{{ item.label }}</button></nav>
        <footer v-if="health" class="status"><i></i> سرویس محلی آماده است</footer>
      </aside>
      <main><header><div><p class="eyebrow">LOCAL COMMERCE CORE</p><h1>{{ title }}</h1></div><button class="refresh" @click="refresh" :disabled="loading">{{ loading ? 'در حال بروزرسانی…' : 'بروزرسانی' }}</button></header>
        <p v-if="error" class="message error">{{ error }}</p><p v-if="notice" class="message success">{{ notice }}</p>
        <template v-if="activeView === 'dashboard'"><section v-if="dashboard" class="metrics"><article><span>فروش خالص</span><strong>{{ money(dashboard.revenue) }}</strong><small>ریال</small></article><article><span>سود خالص</span><strong>{{ money(dashboard.net_profit) }}</strong><small>ریال</small></article><article><span>مطالبات</span><strong>{{ money(dashboard.receivables) }}</strong><small>ریال</small></article><article class="warning"><span>هشدار موجودی</span><strong>{{ money(dashboard.low_stock_count) }}</strong><small>کالا</small></article></section><section class="panel"><h2>خلاصهٔ مالی</h2><dl v-if="dashboard"><div><dt>بهای تمام‌شده</dt><dd>{{ money(dashboard.cogs) }} ریال</dd></div><div><dt>بدهی تأمین‌کنندگان</dt><dd>{{ money(dashboard.payables) }} ریال</dd></div><div><dt>ماندهٔ حساب‌ها</dt><dd>{{ money(dashboard.cash_bank_balance) }} ریال</dd></div></dl></section></template>
        <template v-else-if="activeView === 'products'"><section class="two-col"><form class="panel" @submit.prevent="addProduct"><h2>ثبت کالای جدید</h2><label>نام کالا<input v-model="product.name" required /></label><label>بارکد<input v-model="product.barcode" /></label><div class="form-row"><label>قیمت فروش<input v-model.number="product.retail_price" type="number" min="0" /></label><label>حداقل موجودی<input v-model.number="product.min_stock" type="number" min="0" /></label></div><button class="primary">ثبت کالا</button></form><section class="panel"><h2>کالاها</h2><table><thead><tr><th>کد</th><th>نام</th><th>موجودی</th><th>قیمت فروش</th></tr></thead><tbody><tr v-for="item in products" :key="item.id"><td>{{ item.code }}</td><td>{{ item.name }}</td><td>{{ item.current_stock }}</td><td>{{ money(item.retail_price) }}</td></tr><tr v-if="!products.length"><td colspan="4">هنوز کالایی ثبت نشده است.</td></tr></tbody></table></section></section></template>
        <template v-else-if="activeView === 'inventory'"><section class="panel"><h2>وضعیت موجودی</h2><table><thead><tr><th>کالا</th><th>موجودی فعلی</th><th>حداقل موجودی</th></tr></thead><tbody><tr v-for="item in products" :key="item.id"><td>{{ item.name }}</td><td>{{ item.current_stock }}</td><td>{{ item.min_stock }}</td></tr></tbody></table></section></template>
        <template v-else><section class="panel"><h2>{{ title }}</h2><p class="message">این بخش در حال توسعه است. مسیر آن در برنامه ثبت شده و آماده اتصال به رابط کاربری مربوطه است.</p></section></template>
      </main>
    </div>`
}
createApp(App).mount('#app')
