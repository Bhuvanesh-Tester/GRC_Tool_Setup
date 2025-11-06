import { useEffect, useState, useCallback } from 'react'
import api from '../api/client'
import { supabase } from '../lib/supabase'

export default function useAuth() {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  const fetchMe = useCallback(async () => {
    try {
      const res = await api.get('/api/v1/auth/me')
      setUser(res.data)
    } catch (e) {
      setUser(null)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { fetchMe() }, [fetchMe])

  const login = async ({ role, email, password }) => {
    const demo = (
      import.meta.env.VITE_DEMO_MODE === 'true' ||
      (!import.meta.env.VITE_SUPABASE_URL && !import.meta.env.VITE_SUPABASE_ANON_KEY)
    )
    if (demo) {
      const res = await api.post('/api/v1/auth/login', { role })
      localStorage.setItem('token', res.data.access_token)
      await fetchMe()
      return true
    }
    if (!supabase) return false
    const { data, error } = await supabase.auth.signInWithPassword({ email, password })
    if (error) return false
    const accessToken = data.session?.access_token
    if (!accessToken) return false
    localStorage.setItem('token', accessToken)
    await fetchMe()
    return true
  }

  const logout = async () => {
    localStorage.removeItem('token')
    if (supabase) {
      try { await supabase.auth.signOut() } catch (_) {}
    }
    setUser(null)
  }

  return { user, loading, login, logout }
}