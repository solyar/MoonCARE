<template>
  <nav class="fixed bottom-0 left-0 right-0 bg-white z-50 safe-area-pb" style="box-shadow: 0 -2px 10px rgba(0,0,0,0.05);">
    <div class="flex justify-around items-center h-14 max-w-lg mx-auto relative">
      <!-- Active indicator bar -->
      <div
        class="absolute top-0 h-0.5 bg-gradient-to-r from-blue-500 to-blue-600 transition-all duration-300"
        :style="activeBarStyle"
      ></div>

      <router-link
        v-for="item in navItems"
        :key="item.path"
        :to="item.path"
        class="nav-item flex flex-col items-center justify-center w-full h-full transition-all duration-200"
        :class="isActive(item.path) ? 'text-blue-500' : 'text-gray-400'"
      >
        <span class="nav-icon text-xl mb-0.5 transition-transform duration-200" :class="isActive(item.path) ? 'scale-110' : ''">{{ item.icon }}</span>
        <span class="text-xs font-medium">{{ item.label }}</span>
      </router-link>
    </div>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const navItems = [
  { path: '/', label: '首页', icon: '🏠' },
  { path: '/diary', label: '日记', icon: '📝' },
  { path: '/profile', label: '我的', icon: '👤' }
]

const activeIndex = computed(() => {
  const index = navItems.findIndex(item => {
    if (item.path === '/') {
      return route.path === '/'
    }
    return route.path.startsWith(item.path)
  })
  return index >= 0 ? index : 0
})

const activeBarStyle = computed(() => {
  const width = 100 / navItems.length
  const left = activeIndex.value * width
  return {
    width: `${width}%`,
    left: `${left}%`
  }
})

function isActive(path) {
  if (path === '/') {
    return route.path === '/'
  }
  return route.path.startsWith(path)
}
</script>

<style scoped>
.safe-area-pb {
  padding-bottom: env(safe-area-inset-bottom, 0);
}

.nav-item:active {
  opacity: 0.7;
}
</style>
