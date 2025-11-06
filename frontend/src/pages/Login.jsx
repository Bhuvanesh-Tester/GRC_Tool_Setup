import { useState } from 'react'
import useAuth from '../hooks/useAuth'
import Button from '../components/ui/Button'
import Card from '../components/ui/Card'

const ROLES = [
  { key: 'admin', label: 'Admin' },
  { key: 'risk_manager', label: 'Risk Manager' },
  { key: 'compliance_officer', label: 'Compliance Officer' },
  { key: 'auditor', label: 'Auditor' },
  { key: 'viewer', label: 'Viewer' },
]

export default function Login() {
  const { login } = useAuth()
  const demo = (
    import.meta.env.VITE_DEMO_MODE === 'true' ||
    (!import.meta.env.VITE_SUPABASE_URL && !import.meta.env.VITE_SUPABASE_ANON_KEY)
  )
  const [selected, setSelected] = useState('viewer')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')

  const handleLogin = async () => {
    const ok = await login(demo ? { role: selected } : { email, password })
    if (!ok) setError('Login failed. Check credentials or Supabase config.')
    else window.location.href = '/'
  }

  return (
    <div className="max-w-md mx-auto mt-10">
      <Card>
        <h2 className="text-xl font-semibold mb-4">Login</h2>
        {demo ? (
          <>
            <p className="text-sm text-gray-600 mb-2">Demo mode: choose a role to sign in.</p>
            <select className="border rounded px-3 py-2 w-full mb-4" value={selected} onChange={(e) => setSelected(e.target.value)}>
              {ROLES.map(r => <option key={r.key} value={r.key}>{r.label}</option>)}
            </select>
          </>
        ) : (
          <>
            <p className="text-sm text-gray-600 mb-2">Production: sign in with Supabase email and password.</p>
            <input className="border rounded px-3 py-2 w-full mb-2" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
            <input type="password" className="border rounded px-3 py-2 w-full mb-4" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
          </>
        )}
        {error && <div className="text-red-600 text-sm mb-2">{error}</div>}
        <Button onClick={handleLogin}>Login</Button>
      </Card>
    </div>
  )
}