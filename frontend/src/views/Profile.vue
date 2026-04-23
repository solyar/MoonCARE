<template>
  <div class="profile-page">
    <div class="max-w-lg mx-auto pb-16">
      <!-- Header -->
      <div class="bg-gradient-to-br from-pink-50 to-purple-50 px-4 pt-4 pb-3">
        <h1 class="text-lg font-bold text-gray-800">个人中心</h1>
      </div>

      <!-- User Info Card -->
      <div class="px-4 -mt-2">
        <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
          <div class="flex items-center gap-3">
            <div class="w-12 h-12 rounded-full bg-pink-100 flex items-center justify-center">
              <span class="text-2xl">👤</span>
            </div>
            <div class="flex-1">
              <div class="font-medium text-gray-800">用户 {{ userId }}</div>
              <div class="text-xs text-gray-500">智能情绪管理</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Cycle Section -->
      <div class="px-4 mt-4">
        <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
          <router-link
            to="/cycle"
            class="flex items-center justify-between p-4 active:bg-gray-50"
          >
            <div class="flex items-center gap-3">
              <span class="text-xl">🌼</span>
              <div>
                <div class="font-medium text-gray-800 text-sm">周期记录</div>
                <div class="text-xs text-gray-500">查看月经周期</div>
              </div>
            </div>
            <span class="text-gray-400 text-sm">→</span>
          </router-link>

          <div class="border-t border-gray-100"></div>

          <!-- Cycle Prediction Display -->
          <div v-if="cyclePrediction" class="p-4">
            <div class="flex items-center gap-2 mb-2">
              <span class="text-xl">🔮</span>
              <span class="text-sm font-medium text-gray-700">周期预测</span>
            </div>
            <div class="space-y-1 text-xs text-gray-600 pl-7">
              <div v-if="cyclePrediction.predicted_start">
                下次月经: {{ formatDate(cyclePrediction.predicted_start) }}
              </div>
              <div>
                {{ getPhaseName(cyclePrediction.current_phase) }}
                <span v-if="cyclePrediction.current_phase === 'luteal'">
                  {{ cyclePrediction.phase_days_remaining }}天后可能来潮
                </span>
                <span v-else>
                  {{ cyclePrediction.phase_days_remaining }}天后进入下一阶段
                </span>
              </div>
            </div>
          </div>

          <div class="border-t border-gray-100"></div>

          <router-link
            to="/wave"
            class="flex items-center justify-between p-4 active:bg-gray-50"
          >
            <div class="flex items-center gap-3">
              <span class="text-xl">📊</span>
              <div>
                <div class="font-medium text-gray-800 text-sm">波形监测</div>
                <div class="text-xs text-gray-500">HRV & 温度实时数据</div>
              </div>
            </div>
            <span class="text-gray-400 text-sm">→</span>
          </router-link>
        </div>
      </div>

      <!-- Settings Section -->
      <div class="px-4 mt-4">
        <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
          <div class="flex items-center justify-between p-4 active:bg-gray-50 cursor-pointer">
            <div class="flex items-center gap-3">
              <span class="text-xl">⚙️</span>
              <div>
                <div class="font-medium text-gray-800 text-sm">设置</div>
                <div class="text-xs text-gray-500">通知、隐私等</div>
              </div>
            </div>
            <span class="text-gray-400 text-sm">→</span>
          </div>

          <div class="border-t border-gray-100"></div>

          <div class="flex items-center justify-between p-4 active:bg-gray-50 cursor-pointer">
            <div class="flex items-center gap-3">
              <span class="text-xl">📖</span>
              <div>
                <div class="font-medium text-gray-800 text-sm">使用指南</div>
                <div class="text-xs text-gray-500">了解如何使用</div>
              </div>
            </div>
            <span class="text-gray-400 text-sm">→</span>
          </div>
        </div>
      </div>

      <!-- App Info -->
      <div class="px-4 mt-6 text-center">
        <div class="text-xs text-gray-400">她语 MoonCARE v1.0.0</div>
        <div class="text-xs text-gray-300 mt-1">智能情绪管理平台</div>
      </div>
    </div>

    <!-- Bottom Nav -->
    <BottomNav />
  </div>
</template>

<script setup>
import BottomNav from '../components/BottomNav.vue'
import { ref, computed, onMounted } from 'vue'
import { useHealthStore } from '../stores/health'

const healthStore = useHealthStore()
const userId = ref(1)

const cyclePrediction = computed(() => healthStore.cyclePrediction)

function getPhaseName(phase) {
  const names = {
    follicular: '卵泡期',
    ovulation: '排卵期',
    luteal: '黄体期',
    menstrual: '经期'
  }
  return names[phase] || phase
}

function formatDate(dateStr) {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', { month: 'long', day: 'numeric' })
}

onMounted(async () => {
  await healthStore.fetchCyclePrediction()
})
</script>

<style scoped>
.profile-page {
  min-height: 100vh;
  background: #f9fafb;
}
</style>
