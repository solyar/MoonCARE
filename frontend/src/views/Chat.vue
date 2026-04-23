<template>
  <div class="chat-page">
    <div class="max-w-lg mx-auto pb-16">
      <!-- Header -->
      <div class="flex items-center justify-between px-4 pt-4 pb-2">
        <div class="flex items-center gap-2">
          <span class="text-2xl">
            <svg width="28" height="28" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
              <ellipse cx="16" cy="18" rx="12" ry="10" fill="#FFE5EC"/>
              <ellipse cx="16" cy="18" rx="10" ry="8" fill="#FFCCD5"/>
              <circle cx="12" cy="16" r="2" fill="#5D4E60"/>
              <circle cx="20" cy="16" r="2" fill="#5D4E60"/>
              <circle cx="12.5" cy="15.5" r="0.8" fill="white"/>
              <circle cx="20.5" cy="15.5" r="0.8" fill="white"/>
              <ellipse cx="16" cy="20" rx="1.5" ry="1" fill="#FF8FAB"/>
              <ellipse cx="10" cy="12" rx="3" ry="2" fill="#FFE5EC" opacity="0.8"/>
              <ellipse cx="22" cy="12" rx="3" ry="2" fill="#FFE5EC" opacity="0.8"/>
            </svg>
          </span>
          <div>
            <h1 class="text-base font-bold text-gray-800">情绪宝宝</h1>
          </div>
        </div>
        <button
          v-if="messages.length > 0"
          @click="clearChat"
          class="text-xs text-gray-500 hover:text-gray-700"
        >
          清空对话
        </button>
      </div>

      <!-- Chat Messages -->
      <div ref="messagesContainer" class="px-4 flex-1 overflow-y-auto space-y-3" style="height: calc(100vh - 12rem);">
        <!-- Welcome Message -->
        <div v-if="messages.length === 0" class="flex flex-col items-center justify-center h-full text-center">
          <span class="mb-4">
            <svg width="64" height="64" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
              <ellipse cx="40" cy="45" rx="30" ry="25" fill="#FFE5EC"/>
              <ellipse cx="40" cy="45" rx="25" ry="20" fill="#FFCCD5"/>
              <circle cx="30" cy="40" r="5" fill="#5D4E60"/>
              <circle cx="50" cy="40" r="5" fill="#5D4E60"/>
              <circle cx="31.5" cy="38.5" r="2" fill="white"/>
              <circle cx="51.5" cy="38.5" r="2" fill="white"/>
              <ellipse cx="40" cy="50" rx="4" ry="2.5" fill="#FF8FAB"/>
              <ellipse cx="25" cy="30" rx="7" ry="5" fill="#FFE5EC" opacity="0.8"/>
              <ellipse cx="55" cy="30" rx="7" ry="5" fill="#FFE5EC" opacity="0.8"/>
            </svg>
          </span>
          <h2 class="text-base font-semibold text-gray-700 mb-1">你好，我是情绪宝宝</h2>
          <p class="text-xs text-gray-500 max-w-xs">
            有什么想说的都可以告诉我，我会一直陪着你~
          </p>
        </div>

        <!-- Messages -->
        <div
          v-for="msg in messages"
          :key="msg.id"
          class="flex animate-fadeIn"
          :class="msg.role === 'user' ? 'justify-end' : 'justify-start'"
        >
          <div
            class="max-w-[80%] rounded-2xl px-3 py-2"
            :class="msg.role === 'user'
              ? 'bg-gradient-to-br from-pink-500 to-pink-600 text-white rounded-br-md'
              : 'bg-white border border-gray-100 text-gray-700 rounded-bl-md'"
          >
            <p class="text-sm leading-relaxed whitespace-pre-wrap">{{ msg.content }}</p>

            <!-- Suggestions -->
            <div v-if="msg.role === 'assistant' && msg.suggestions && msg.suggestions.length > 0" class="mt-1.5 flex flex-wrap gap-1">
              <button
                v-for="suggestion in msg.suggestions"
                :key="suggestion"
                @click="handleSuggestion(suggestion)"
                class="px-2 py-0.5 text-xs rounded-full transition-colors"
                :class="isDarkMode
                  ? 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                  : 'bg-pink-50 text-pink-600 hover:bg-pink-100'"
              >
                {{ suggestion }}
              </button>
            </div>

            <span
              class="text-xs mt-0.5 block"
              :class="msg.role === 'user' ? 'text-pink-200' : 'text-gray-400'"
            >
              {{ formatTime(msg.timestamp) }}
            </span>
          </div>
        </div>

        <!-- Typing Indicator -->
        <div v-if="isTyping" class="flex justify-start">
          <div class="bg-white border border-gray-100 rounded-2xl rounded-bl-md px-3 py-2">
            <div class="flex gap-1">
              <span class="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0ms"></span>
              <span class="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 150ms"></span>
              <span class="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 300ms"></span>
            </div>
          </div>
        </div>
      </div>

      <!-- Input Area -->
      <div class="px-4 pb-4">
        <div class="bg-white rounded-xl border border-gray-200 p-2">
          <div class="flex items-end gap-2">
            <div class="flex-1">
              <textarea
                v-model="inputMessage"
                @keydown.enter.exact.prevent="sendMessage"
                class="w-full p-2 border border-gray-200 rounded-lg resize-none focus:ring-2 focus:ring-pink-200 focus:border-pink-400 outline-none text-sm"
                rows="1"
                placeholder="输入消息..."
              ></textarea>
            </div>
            <button
              @click="sendMessage"
              :disabled="!inputMessage.trim() || isTyping"
              class="p-2 rounded-lg transition-colors"
              :class="inputMessage.trim()
                ? 'bg-pink-500 text-white hover:bg-pink-600'
                : 'bg-gray-100 text-gray-400 cursor-not-allowed'"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Bottom Nav -->
    <BottomNav />
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted, onUnmounted, computed, watch } from 'vue'
import { useChatStore } from '../stores/chat'
import { useRouter } from 'vue-router'
import { chatAPI, interviewAPI } from '../api'
import BottomNav from '../components/BottomNav.vue'

const chatStore = useChatStore()
const router = useRouter()

const messagesContainer = ref(null)
const inputMessage = ref('')
const isTyping = ref(false)
const currentSessionId = ref(null)

const messages = computed(() => chatStore.messages)
const isConnected = computed(() => chatStore.isConnected)
const isDarkMode = ref(false)

// Auto-scroll when messages change
watch(messages, async () => {
  await nextTick()
  scrollToBottom()
}, { deep: true })

function formatTime(timestamp) {
  if (!timestamp) return ''
  return new Date(timestamp).toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

async function sendMessage() {
  const text = inputMessage.value.trim()
  if (!text || isTyping.value) return

  inputMessage.value = ''

  // Add user message
  chatStore.addMessage(text, 'user')

  // Show typing indicator
  isTyping.value = true

  // Try WebSocket first, fall back to REST API
  try {
    if (chatStore.isInterviewMode) {
      // Interview mode - use interview API
      const messages = chatStore.messages.map(m => ({ role: m.role, content: m.content }))
      const result = await interviewAPI.turn(messages, 1)
      if (result.crisis) {
        // Crisis detected, intervention agent responded
        chatStore.addAssistantMessage(result.reply, [])
        chatStore.endInterview()
      } else {
        chatStore.addAssistantMessage(result.reply, [])
        if (result.is_complete) {
          chatStore.endInterview()
          if (result.report) {
            chatStore.addAssistantMessage(`访谈已完成。\n\n${result.report}`, [])
          } else if (result.psst) {
            chatStore.addAssistantMessage(`访谈已完成。`, [])
          }
        } else {
          chatStore.interviewPhase = result.phase
        }
      }
    } else if (chatStore.isConnected) {
      chatStore.sendMessage(text)
      // For WebSocket, response comes asynchronously, so we need to wait for it
      // The watch on messages will handle scrolling when response arrives
    } else {
      // Use REST API to call SupportAgent
      console.log('Sending message to API:', text)
      const result = await chatAPI.sendMessage(text, 1, currentSessionId.value)
      console.log('API response:', result)
      currentSessionId.value = result.session_id
      chatStore.addAssistantMessage(result.reply, result.suggestions || [])
    }
  } catch (error) {
    console.error('Failed to send message:', error)
    console.error('Error response:', error.response)
    chatStore.addAssistantMessage('抱歉，我现在有点状况，可能需要稍后再试~', [])
  }

  isTyping.value = false
}

function handleSuggestion(suggestion) {
  const text = {
    '深呼吸': '我想试试深呼吸练习',
    '散步': '我想出门走走',
    '听音乐': '我想听点舒缓的音乐'
  }[suggestion] || suggestion

  inputMessage.value = text
  sendMessage()
}

function clearChat() {
  chatStore.clearMessages()
}

function scrollToBottom() {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

onMounted(async () => {
  // Skip session creation in interview mode - interview API handles its own state
  if (chatStore.isInterviewMode) {
    return
  }
  // Try to create session via REST API (handled in sendMessage if needed)
  try {
    const session = await chatStore.createSession()
    currentSessionId.value = session
  } catch (error) {
    console.log('Session will be created on first message')
  }
})

onUnmounted(() => {
  // Don't disconnect on unmount to preserve session
})
</script>

<style scoped>
.chat-page {
  min-height: 100vh;
  background: #f9fafb;
}
</style>
