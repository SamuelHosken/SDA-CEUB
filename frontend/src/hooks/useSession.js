import { useState, useEffect } from 'react'
import { auth } from '../services/firebase'
export function useSession() {
  const [sessionId, setSessionId] = useState(null)
  useEffect(() => {
    const unsubscribe = auth.onAuthStateChanged((user) => {
      if (user) {
        setSessionId(user.uid)
      } else {
        let session = localStorage.getItem('sda_session_id')
        if (!session) {
          session = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
          localStorage.setItem('sda_session_id', session)
        }
        setSessionId(session)
      }
    })
    return () => unsubscribe()
  }, [])
  return { sessionId }
}