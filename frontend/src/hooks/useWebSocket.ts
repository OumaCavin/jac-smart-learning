import { useEffect, useState } from 'react'
import { io, Socket } from 'socket.io-client'

interface WebSocketState {
  socket: Socket | null
  isConnected: boolean
  connectionStatus: 'connecting' | 'connected' | 'disconnected' | 'error'
  error: string | null
  lastMessage: any
}

interface UseWebSocketReturn extends WebSocketState {
  emit: (event: string, data?: any) => void
  subscribe: (event: string, callback: (data: any) => void) => () => void
  disconnect: () => void
  reconnect: () => void
}

const SOCKET_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000'

export const useWebSocket = (): UseWebSocketReturn => {
  const [socket, setSocket] = useState<Socket | null>(null)
  const [isConnected, setIsConnected] = useState(false)
  const [connectionStatus, setConnectionStatus] = useState<WebSocketState['connectionStatus']>('disconnected')
  const [error, setError] = useState<string | null>(null)
  const [lastMessage, setLastMessage] = useState<any>(null)

  useEffect(() => {
    // Create socket connection
    const socketInstance = io(SOCKET_URL, {
      transports: ['websocket'],
      timeout: 5000,
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionAttempts: 5,
      maxReconnectionAttempts: 5
    })

    // Connection event handlers
    socketInstance.on('connect', () => {
      console.log('WebSocket connected')
      setIsConnected(true)
      setConnectionStatus('connected')
      setError(null)
    })

    socketInstance.on('disconnect', (reason) => {
      console.log('WebSocket disconnected:', reason)
      setIsConnected(false)
      setConnectionStatus('disconnected')
    })

    socketInstance.on('connect_error', (err) => {
      console.error('WebSocket connection error:', err)
      setError(err.message)
      setConnectionStatus('error')
    })

    socketInstance.on('reconnect_attempt', () => {
      setConnectionStatus('connecting')
    })

    socketInstance.on('reconnect', () => {
      setConnectionStatus('connected')
      setError(null)
    })

    socketInstance.on('reconnect_error', (err) => {
      setError(`Reconnection failed: ${err.message}`)
    })

    // Set initial state
    setSocket(socketInstance)
    setConnectionStatus('connecting')

    // Cleanup on unmount
    return () => {
      if (socketInstance) {
        socketInstance.disconnect()
      }
    }
  }, [])

  // Subscribe to common events
  useEffect(() => {
    if (!socket) return

    // Agent status updates
    const handleAgentUpdate = (data: any) => {
      console.log('Agent update received:', data)
      setLastMessage({ type: 'agent_update', data })
    }

    // Task completion events
    const handleTaskCompleted = (data: any) => {
      console.log('Task completed:', data)
      setLastMessage({ type: 'task_completed', data })
    }

    // System health updates
    const handleSystemHealth = (data: any) => {
      console.log('System health update:', data)
      setLastMessage({ type: 'system_health', data })
    }

    // Error events
    const handleError = (data: any) => {
      console.error('System error:', data)
      setLastMessage({ type: 'error', data })
    }

    // Subscribe to events
    socket.on('agent:update', handleAgentUpdate)
    socket.on('task:completed', handleTaskCompleted)
    socket.on('system:health', handleSystemHealth)
    socket.on('error', handleError)

    // Cleanup subscriptions
    return () => {
      socket.off('agent:update', handleAgentUpdate)
      socket.off('task:completed', handleTaskCompleted)
      socket.off('system:health', handleSystemHealth)
      socket.off('error', handleError)
    }
  }, [socket])

  const emit = (event: string, data?: any) => {
    if (socket && isConnected) {
      socket.emit(event, data)
    } else {
      console.warn('Cannot emit: WebSocket not connected')
    }
  }

  const subscribe = (event: string, callback: (data: any) => void) => {
    if (!socket) {
      console.warn('Cannot subscribe: WebSocket not initialized')
      return () => {}
    }

    socket.on(event, callback)
    
    // Return unsubscribe function
    return () => {
      socket.off(event, callback)
    }
  }

  const disconnect = () => {
    if (socket) {
      socket.disconnect()
    }
  }

  const reconnect = () => {
    if (socket) {
      socket.connect()
    }
  }

  return {
    socket,
    isConnected,
    connectionStatus,
    error,
    lastMessage,
    emit,
    subscribe,
    disconnect,
    reconnect
  }
}

// Custom hook for specific WebSocket patterns

export const useAgentUpdates = () => {
  const { subscribe, isConnected } = useWebSocket()
  const [agentUpdates, setAgentUpdates] = useState<any[]>([])

  useEffect(() => {
    if (!isConnected) return

    const unsubscribe = subscribe('agent:update', (data) => {
      setAgentUpdates(prev => [data, ...prev.slice(0, 99)]) // Keep last 100 updates
    })

    return unsubscribe
  }, [isConnected, subscribe])

  return agentUpdates
}

export const useTaskNotifications = () => {
  const { subscribe, isConnected } = useWebSocket()
  const [taskNotifications, setTaskNotifications] = useState<any[]>([])

  useEffect(() => {
    if (!isConnected) return

    const unsubscribe = subscribe('task:completed', (data) => {
      setTaskNotifications(prev => [data, ...prev.slice(0, 49)]) // Keep last 50 notifications
    })

    return unsubscribe
  }, [isConnected, subscribe])

  return taskNotifications
}

export const useSystemHealth = () => {
  const { subscribe, isConnected } = useWebSocket()
  const [systemHealth, setSystemHealth] = useState<any>(null)

  useEffect(() => {
    if (!isConnected) return

    const unsubscribe = subscribe('system:health', (data) => {
      setSystemHealth(data)
    })

    return unsubscribe
  }, [isConnected, subscribe])

  return systemHealth
}

// WebSocket connection utility functions

export const createSocketConnection = (url: string, options?: any) => {
  return io(url, {
    transports: ['websocket'],
    timeout: 5000,
    reconnection: true,
    reconnectionDelay: 1000,
    reconnectionAttempts: 5,
    maxReconnectionAttempts: 5,
    ...options
  })
}

export const pingSocket = async (socket: Socket): Promise<boolean> => {
  return new Promise((resolve) => {
    const timeout = setTimeout(() => resolve(false), 5000)
    
    socket.emit('ping', (response: any) => {
      clearTimeout(timeout)
      resolve(response === 'pong')
    })
  })
}