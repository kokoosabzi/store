/* Store workspace tabs use stable router IDs, never visible menu labels, as identity. */
import { router, navigate } from './router.js'

;(() => {
  'use strict'
  const storageKey = 'lcc.workspace.tabs.v2'
  const host = () => document.getElementById('koko-workspace-tabs')
  const routes = router.routes
  const routeById = id => routes.find(route => route.id === id)
  const currentRoute = () => router.current()
  const read = () => {
    try {
      const saved = JSON.parse(sessionStorage.getItem(storageKey) || '[]')
      if (!Array.isArray(saved)) return []
      return saved
        .filter(item => item && typeof item.id === 'string' && routeById(item.id))
        .map(item => ({ id: item.id }))
        .slice(-8)
    } catch {
      return []
    }
  }
  let tabs = read()

  const save = () => {
    try {
      sessionStorage.setItem(storageKey, JSON.stringify(tabs.slice(-8)))
    } catch {
      // Storage may be unavailable in private browsing; tabs still work in memory.
    }
  }

  const ensureCurrent = () => {
    const route = currentRoute()
    if (!tabs.some(tab => tab.id === route.id)) tabs.push({ id: route.id })
    tabs = tabs.slice(-8)
    save()
  }

  const activate = id => {
    const route = routeById(id)
    if (route) navigate(route.path)
  }

  const render = () => {
    const element = host()
    if (!element) return
    const currentId = currentRoute().id
    element.replaceChildren()

    tabs.forEach(tab => {
      const route = routeById(tab.id)
      if (!route) return

      const item = document.createElement('div')
      item.className = 'koko-tab' + (tab.id === currentId ? ' active' : '')

      const activateButton = document.createElement('button')
      activateButton.type = 'button'
      activateButton.textContent = route.label
      activateButton.setAttribute('aria-current', tab.id === currentId ? 'page' : 'false')
      activateButton.addEventListener('click', () => activate(tab.id))

      const closeButton = document.createElement('button')
      closeButton.type = 'button'
      closeButton.className = 'koko-tab-close'
      closeButton.textContent = '×'
      closeButton.setAttribute('aria-label', 'بستن ' + route.label)
      closeButton.addEventListener('click', () => {
        const index = tabs.findIndex(item => item.id === tab.id)
        tabs = tabs.filter(item => item.id !== tab.id)
        if (tab.id === currentId) {
          const next = tabs[Math.min(index, tabs.length - 1)]
          save()
          activate(next?.id || 'dashboard')
          return
        }
        save()
        render()
      })

      item.append(activateButton, closeButton)
      element.append(item)
    })
  }

  const sync = () => {
    ensureCurrent()
    render()
  }

  window.addEventListener('route-change', sync)
  window.addEventListener('storage', event => {
    if (event.key === storageKey) {
      tabs = read()
      sync()
    }
  })

  sync()
})()
