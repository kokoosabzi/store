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
    const customers = ref([])
    const accounts = ref([])
    const sales = ref([])
    const error = ref('')
    const notice = ref('')
    const loading = ref(false)
    const product = ref({ name: '', barcode: '', retail_price: 0, min_stock: 0 })
    const cart = ref([])
    const saleCustomer = ref('')
    const saleAccount = ref('')
    const salePaid = ref(0)
    const saleDiscount = ref(0)
    const saleTax = ref(0)
    const saleProductId = ref('')
    const saleQuantity = ref(1)
    const saleSearch = ref('')
    const nav = router.routes

    const title = computed(() => nav.find(item => item.id === activeView.value)?.label || '')
    const money = value => new Intl.NumberFormat('fa-IR').format(Number(value || 0))
    const filteredSaleProducts = computed(() => {
      const q = saleSearch.value.trim().toLowerCase()
      if (!q) return products.value
      return products.value.filter(item =>
        String(item.name || '').toLowerCase().includes(q) ||
        String(item.code || '').toLowerCase().includes(q) ||
        String(item.barcode || '').toLowerCase().includes(q)
      )
    })
    const cartSubtotal = computed(() => cart.value.reduce((sum, item) => sum + item.quantity * item.unit_price - item.discount, 0))
    const saleTotal = computed(() => Math.max(0, cartSubtotal.value - Number(saleDiscount.value || 0) + Number(saleTax.value || 0)))
    const saleRemaining = computed(() => Math.max(0, saleTotal.value - Number(salePaid.value || 0)))

    const loadProducts = async () => { products.value = await api('/products') }
    const loadDashboard = async () => { dashboard.value = await api('/dashboard') }
    const loadCustomers = async () => { customers.value = await api('/customers') }
    const loadAccounts = async () => { accounts.value = await api('/accounts') }
    const loadSales = async () => { sales.value = await api('/sales') }

    const refresh = async () => {
      loading.value = true; error.value = ''
      try {
        health.value = await api('/health')
        await Promise.all([loadDashboard(), loadProducts(), loadCustomers(), loadAccounts(), loadSales()])
      } catch (err) { error.value = err.message }
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

    const addToCart = () => {
      error.value = ''; notice.value = ''
      const item = products.value.find(item => item.id === Number(saleProductId.value))
      const quantity = Number(saleQuantity.value)
      if (!item) { error.value = 'یک کالا انتخاب کنید.'; return }
      if (!quantity || quantity <= 0) { error.value = 'تعداد معتبر وارد کنید.'; return }
      const existing = cart.value.find(line => line.product_id === item.id)
      if (existing) existing.quantity += quantity
      else cart.value.push({ product_id: item.id, name: item.name, quantity, unit_price: Number(item.retail_price || 0), discount: 0, stock: Number(item.current_stock || 0) })
      saleProductId.value = ''; saleQuantity.value = 1
    }

    const removeFromCart = productId => { cart.value = cart.value.filter(item => item.product_id !== productId) }

    const clearSale = () => {
      cart.value = []; saleCustomer.value = ''; salePaid.value = 0; saleDiscount.value = 0; saleTax.value = 0
      saleProductId.value = ''; saleQuantity.value = 1; error.value = ''; notice.value = ''
    }

    const createAccount = async () => {
      error.value = ''; notice.value = ''
      try {
        const created = await api('/accounts?name=' + encodeURIComponent('صندوق') + '&account_type=cash', { method: 'POST' })
        await loadAccounts(); saleAccount.value = String(created.id); notice.value = 'حساب صندوق ایجاد شد.'
      } catch (err) { error.value = err.message }
    }

    const finalizeSale = async () => {
      error.value = ''; notice.value = ''
      if (!cart.value.length) { error.value = 'سبد فروش خالی است.'; return }
      if (Number(salePaid.value || 0) > saleTotal.value) { error.value = 'مبلغ دریافتی از مبلغ فروش بیشتر است.'; return }
      if (Number(salePaid.value || 0) > 0 && !saleAccount.value) { error.value = 'برای فروش نقدی، حساب دریافت را انتخاب کنید.'; return }
      if (saleRemaining.value > 0 && !saleCustomer.value) { error.value = 'برای فروش اعتباری، مشتری را انتخاب کنید.'; return }
      loading.value = true
      try {
        const draft = await api('/sales/draft', {
          method: 'POST',
          body: JSON.stringify({
            customer_id: saleCustomer.value ? Number(saleCustomer.value) : null,
            items: cart.value.map(item => ({ product_id: item.product_id, quantity: item.quantity, unit_price: item.unit_price, discount: item.discount })),
            discount: Number(saleDiscount.value || 0),
            tax: Number(saleTax.value || 0),
            paid_amount: Number(salePaid.value || 0),
            account_id: saleAccount.value ? Number(saleAccount.value) : null
          })
        })
        await api(`/sales/${draft.id}/finalize${saleAccount.value ? `?account_id=${Number(saleAccount.value)}` : ''}`, { method: 'POST' })
        notice.value = 'فروش با موفقیت ثبت و نهایی شد.'
        clearSale()
        await Promise.all([loadProducts(), loadDashboard(), loadSales()])
      } catch (err) { error.value = err.message }
      finally { loading.value = false }
    }

    onMounted(() => {
      const syncRoute = () => { activeView.value = router.current().id }
      window.addEventListener('popstate', syncRoute)
      syncRoute(); refresh()
    })

    return {
      activeView, health, dashboard, products, customers, accounts, sales, error, notice, loading, product,
      cart, saleCustomer, saleAccount, salePaid, saleDiscount, saleTax, saleProductId, saleQuantity, saleSearch,
      nav, title, money, filteredSaleProducts, cartSubtotal, saleTotal, saleRemaining, refresh, addProduct,
      addToCart, removeFromCart, clearSale, createAccount, finalizeSale, navigate
    }
  },
  template: `
    <div class="app-shell">
      <aside class="sidebar">
        <div class="brand"><span>LC</span><strong>هسته بازرگانی</strong><small>محلی و آفلاین</small></div>
        <nav><button v-for="item in nav" :key="item.id" :class="{active: activeView === item.id}" @click="navigate(item.path)">{{ item.label }}</button></nav>
        <footer v-if="health" class="status"><i></i> سرویس محلی آماده است</footer>
      </aside>
      <main>
        <header><div><p class="eyebrow">LOCAL COMMERCE CORE</p><h1>{{ title }}</h1></div><button class="refresh" @click="refresh" :disabled="loading">{{ loading ? 'در حال بروزرسانی…' : 'بروزرسانی' }}</button></header>
        <p v-if="error" class="message error">{{ error }}</p><p v-if="notice" class="message success">{{ notice }}</p>

        <template v-if="activeView === 'dashboard'">
          <section v-if="dashboard" class="metrics"><article><span>فروش خالص</span><strong>{{ money(dashboard.revenue) }}</strong><small>ریال</small></article><article><span>سود خالص</span><strong>{{ money(dashboard.net_profit) }}</strong><small>ریال</small></article><article><span>مطالبات</span><strong>{{ money(dashboard.receivables) }}</strong><small>ریال</small></article><article class="warning"><span>هشدار موجودی</span><strong>{{ money(dashboard.low_stock_count) }}</strong><small>کالا</small></article></section>
          <section class="panel"><h2>خلاصهٔ مالی</h2><dl v-if="dashboard"><div><dt>بهای تمام‌شده</dt><dd>{{ money(dashboard.cogs) }} ریال</dd></div><div><dt>بدهی تأمین‌کنندگان</dt><dd>{{ money(dashboard.payables) }} ریال</dd></div><div><dt>ماندهٔ حساب‌ها</dt><dd>{{ money(dashboard.cash_bank_balance) }} ریال</dd></div></dl></section>
        </template>

        <template v-else-if="activeView === 'products'">
          <section class="two-col"><form class="panel" @submit.prevent="addProduct"><h2>ثبت کالای جدید</h2><label>نام کالا<input v-model="product.name" required /></label><label>بارکد<input v-model="product.barcode" /></label><div class="form-row"><label>قیمت فروش<input v-model.number="product.retail_price" type="number" min="0" /></label><label>حداقل موجودی<input v-model.number="product.min_stock" type="number" min="0" /></label></div><button class="primary">ثبت کالا</button></form>
          <section class="panel"><h2>کالاها</h2><table><thead><tr><th>کد</th><th>نام</th><th>موجودی</th><th>قیمت فروش</th></tr></thead><tbody><tr v-for="item in products" :key="item.id"><td>{{ item.code }}</td><td>{{ item.name }}</td><td>{{ item.current_stock }}</td><td>{{ money(item.retail_price) }}</td></tr><tr v-if="!products.length"><td colspan="4">هنوز کالایی ثبت نشده است.</td></tr></tbody></table></section></section>
        </template>

        <template v-else-if="activeView === 'inventory'">
          <section class="panel"><h2>وضعیت موجودی</h2><table><thead><tr><th>کالا</th><th>موجودی فعلی</th><th>حداقل موجودی</th></tr></thead><tbody><tr v-for="item in products" :key="item.id"><td>{{ item.name }}</td><td>{{ item.current_stock }}</td><td>{{ item.min_stock }}</td></tr><tr v-if="!products.length"><td colspan="3">موردی وجود ندارد.</td></tr></tbody></table></section>
        </template>

        <template v-else-if="activeView === 'sales'">
          <section class="sales-layout">
            <section class="panel">
              <div class="section-head"><h2>فاکتور فروش</h2><button class="secondary" type="button" @click="clearSale">پاک کردن</button></div>
              <div class="form-row"><label>جستجوی کالا<input v-model="saleSearch" placeholder="نام، کد یا بارکد" /></label><label>تعداد<input v-model.number="saleQuantity" type="number" min="0.001" step="0.001" /></label></div>
              <div class="form-row"><label>انتخاب کالا<select v-model="saleProductId"><option value="">انتخاب کنید</option><option v-for="item in filteredSaleProducts" :key="item.id" :value="item.id">{{ item.name }} — {{ money(item.retail_price) }}</option></select></label><div class="action-field"><span>&nbsp;</span><button class="primary" type="button" @click="addToCart">افزودن به فاکتور</button></div></div>
              <table><thead><tr><th>کالا</th><th>تعداد</th><th>قیمت</th><th>جمع</th><th></th></tr></thead><tbody><tr v-for="item in cart" :key="item.product_id"><td>{{ item.name }}</td><td>{{ item.quantity }}</td><td>{{ money(item.unit_price) }}</td><td>{{ money(item.quantity * item.unit_price - item.discount) }}</td><td><button class="icon-button" type="button" @click="removeFromCart(item.product_id)">حذف</button></td></tr><tr v-if="!cart.length"><td colspan="5">هنوز کالایی به فاکتور اضافه نشده است.</td></tr></tbody></table>
            </section>

            <section class="panel">
              <h2>تسویه فروش</h2>
              <label>مشتری <select v-model="saleCustomer"><option value="">مشتری نقدی / بدون مشتری</option><option v-for="item in customers" :key="item.id" :value="item.id">{{ item.name }} — مانده {{ money(item.balance) }}</option></select></label>
              <label>حساب دریافت <select v-model="saleAccount"><option value="">انتخاب حساب</option><option v-for="item in accounts" :key="item.id" :value="item.id">{{ item.name }} — {{ money(item.current_balance) }} ریال</option></select></label>
              <button v-if="!accounts.length" class="secondary full" type="button" @click="createAccount">ایجاد حساب صندوق</button>
              <div class="form-row"><label>تخفیف فاکتور<input v-model.number="saleDiscount" type="number" min="0" /></label><label>مالیات<input v-model.number="saleTax" type="number" min="0" /></label></div>
              <label>مبلغ دریافتی<input v-model.number="salePaid" type="number" min="0" :max="saleTotal" /></label>
              <dl class="totals"><div><dt>جمع کالاها</dt><dd>{{ money(cartSubtotal) }} ریال</dd></div><div><dt>مبلغ نهایی</dt><dd>{{ money(saleTotal) }} ریال</dd></div><div><dt>مانده مشتری</dt><dd>{{ money(saleRemaining) }} ریال</dd></div></dl>
              <button class="primary full" type="button" :disabled="loading || !cart.length" @click="finalizeSale">ثبت و نهایی‌سازی فروش</button>
            </section>
          </section>
          <section class="panel"><h2>فروش‌های اخیر</h2><table><thead><tr><th>شماره</th><th>تاریخ</th><th>مبلغ</th><th>وضعیت</th></tr></thead><tbody><tr v-for="item in sales.slice(0,10)" :key="item.id"><td>{{ item.document_number || 'پیش‌نویس' }}</td><td>{{ item.created_at ? new Date(item.created_at).toLocaleString('fa-IR') : '-' }}</td><td>{{ money(item.total) }} ریال</td><td>{{ item.status === 'finalized' ? 'نهایی' : 'پیش‌نویس' }}</td></tr><tr v-if="!sales.length"><td colspan="4">هنوز فروشی ثبت نشده است.</td></tr></tbody></table></section>
        </template>

        <template v-else><section class="panel"><h2>{{ title }}</h2><p class="message">این بخش در حال توسعه است. مسیر آن در برنامه ثبت شده و آماده اتصال به رابط کاربری مربوطه است.</p></section></template>
      </main>
    </div>`
}
createApp(App).mount('#app')
