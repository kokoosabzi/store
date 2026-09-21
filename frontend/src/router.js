const routes = [
  { path: '/', id: 'dashboard', label: 'داشبورد' },
  { path: '/products', id: 'products', label: 'کالاها' },
  { path: '/inventory', id: 'inventory', label: 'موجودی' },
  { path: '/sales', id: 'sales', label: 'فروش' },
  { path: '/purchases', id: 'purchases', label: 'خرید' },
  { path: '/customers', id: 'customers', label: 'مشتریان' },
  { path: '/suppliers', id: 'suppliers', label: 'تأمین‌کنندگان' },
  { path: '/payments', id: 'payments', label: 'دریافت و پرداخت' },
  { path: '/returns', id: 'returns', label: 'برگشت‌ها' },
  { path: '/reports', id: 'reports', label: 'گزارش‌ها' },
  { path: '/settings', id: 'settings', label: 'تنظیمات' },
  { path: '/backup', id: 'backup', label: 'پشتیبان‌گیری' },
]

const normalizePath = path => {
  const clean = path.replace(/\/+$/, '') || '/'
  return clean
}

const findRoute = path => routes.find(route => route.path === normalizePath(path)) || routes[0]

export const router = {
  routes,
  current: () => findRoute(window.location.pathname),
  push(path) {
    const route = findRoute(path)
    window.history.pushState({}, '', route.path)
    window.dispatchEvent(new PopStateEvent('popstate'))
  },
  start() {
    const onPopState = () => window.dispatchEvent(new CustomEvent('route-change'))
    window.addEventListener('popstate', onPopState)
    return () => window.removeEventListener('popstate', onPopState)
  },
}

export const navigate = path => router.push(path)
