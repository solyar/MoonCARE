import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue')
  },
  {
    path: '/home-old',
    name: 'HomeOld',
    component: () => import('../views/HomeOld.vue')
  },
  {
    path: '/diary',
    name: 'Diary',
    component: () => import('../views/Diary.vue')
  },
  {
    path: '/cycle',
    name: 'Cycle',
    component: () => import('../views/Cycle.vue')
  },
  {
    path: '/chat',
    name: 'Chat',
    component: () => import('../views/Chat.vue')
  },
  {
    path: '/breathing',
    name: 'Breathing',
    component: () => import('../views/Breathing.vue')
  },
  {
    path: '/music',
    name: 'Music',
    component: () => import('../views/MusicPlayer.vue')
  },
  {
    path: '/wave',
    name: 'WaveMonitor',
    component: () => import('../views/WaveMonitor.vue')
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../views/Profile.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
