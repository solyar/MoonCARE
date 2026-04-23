import { defineStore } from 'pinia'
import { ref } from 'vue'
import { chatAPI } from '../api'

export const useChatStore = defineStore('chat', () => {
  // State
  const messages = ref([])
  const sessionId = ref(null)
  const isConnected = ref(false)
  const isLoading = ref(false)
  const websocket = ref(null)
  // Interview state
  const isInterviewMode = ref(false)
  const interviewPhase = ref(1)

  // Actions
  function addMessage(message, role = 'user') {
    messages.value.push({
      id: Date.now(),
      content: message,
      role,
      timestamp: new Date().toISOString()
    })
  }

  function addAssistantMessage(message, suggestions = []) {
    messages.value.push({
      id: Date.now(),
      content: message,
      role: 'assistant',
      suggestions,
      timestamp: new Date().toISOString()
    })
  }

  async function createSession(userId = 1) {
    try {
      const result = await chatAPI.createSession(userId)
      sessionId.value = result.session_id
      messages.value = []
      return result.session_id
    } catch (error) {
      console.error('Failed to create session:', error)
      throw error
    }
  }

  function connectWebSocket(userId = 1) {
    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const wsUrl = `${wsProtocol}//${window.location.host}/api/v1/chat/ws/${userId}`

    websocket.value = new WebSocket(wsUrl)

    websocket.value.onopen = () => {
      isConnected.value = true
      console.log('WebSocket connected')
    }

    websocket.value.onmessage = (event) => {
      const data = JSON.parse(event.data)

      if (data.type === 'session') {
        sessionId.value = data.session_id
      } else if (data.type === 'assistant') {
        addAssistantMessage(data.message, data.suggestions)
      } else if (data.type === 'error') {
        console.error('WebSocket error:', data.message)
      }
    }

    websocket.value.onclose = () => {
      isConnected.value = false
      console.log('WebSocket disconnected')
    }

    websocket.value.onerror = (error) => {
      console.error('WebSocket error:', error)
      isConnected.value = false
    }
  }

  function sendMessage(message) {
    if (websocket.value && isConnected.value) {
      addMessage(message, 'user')
      websocket.value.send(JSON.stringify({ message }))
    }
  }

  function disconnect() {
    if (websocket.value) {
      websocket.value.close()
      websocket.value = null
    }
    isConnected.value = false
    sessionId.value = null
    messages.value = []
  }

  function clearMessages() {
    messages.value = []
  }

  function setInterviewMode(enabled, phase = 1) {
    isInterviewMode.value = enabled
    interviewPhase.value = phase
  }

  function endInterview() {
    isInterviewMode.value = false
    interviewPhase.value = 1
  }

  return {
    // State
    messages,
    sessionId,
    isConnected,
    isLoading,
    isInterviewMode,
    interviewPhase,
    // Actions
    addMessage,
    addAssistantMessage,
    createSession,
    connectWebSocket,
    sendMessage,
    disconnect,
    clearMessages,
    setInterviewMode,
    endInterview
  }
})
