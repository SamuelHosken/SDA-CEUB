import axios from 'axios'
const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
})
export const chatAPI = {
  conversar: async (mensagem, sessionId) => {
    const response = await api.post('/conversar', {
      mensagem,
      session_id: sessionId,
    })
    return response.data
  },
  getStatus: async (sessionId) => {
    const response = await api.get('/status', {
      params: { session_id: sessionId },
    })
    return response.data
  },
  processarAudio: async (audioFile, sessionId) => {
    const formData = new FormData()
    formData.append('audio', audioFile, 'audio.webm')
    if (sessionId) {
      formData.append('session_id', sessionId)
    }
    const response = await api.post('/audio', formData, {
    })
    return response.data
  },
  resetar: async (sessionId) => {
    const response = await api.post('/resetar', null, {
      params: { session_id: sessionId },
    })
    return response.data
  },
  verifyToken: async (idToken) => {
    const response = await api.post('/auth/verify-token', {
      id_token: idToken,
    })
    return response.data
  },
  getCurrentUser: async () => {
    const token = localStorage.getItem('auth_token')
    const response = await api.get('/auth/me', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
    return response.data
  },
}
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    } else {
      const currentPath = window.location.pathname
      if (typeof window !== 'undefined' &&
        currentPath !== '/' &&
        !currentPath.includes('/login') &&
        !currentPath.includes('/signup')) {
        localStorage.removeItem('auth_token')
        localStorage.removeItem('user')
        localStorage.removeItem('sda_session_id')
        window.location.href = '/login'
        return Promise.reject(new Error('Token não encontrado'))
      }
    }
    if (config.data instanceof FormData) {
      delete config.headers['Content-Type']
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401 || error.response?.status === 403) {
      const currentPath = window.location.pathname
      if (typeof window !== 'undefined' &&
        currentPath !== '/' &&
        !currentPath.includes('/login') &&
        !currentPath.includes('/signup')) {
        localStorage.removeItem('auth_token')
        localStorage.removeItem('user')
        localStorage.removeItem('sda_session_id')
        window.location.href = '/login'
      }
    }
    return Promise.reject(error)
  }
)
export default api