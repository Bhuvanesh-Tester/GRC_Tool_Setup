import { Link, useNavigate } from 'react-router-dom'
import useAuth from '../hooks/useAuth'

export default function Navbar() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  return (
    <nav className="bg-white shadow">
      <div className="container mx-auto px-4 py-3 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Link to="/" className="font-semibold">GRC Platform</Link>
          {user && (
            <>
              <Link to="/policies" className="text-sm">Policies</Link>
              <Link to="/risks" className="text-sm">Risks</Link>
              <Link to="/compliance" className="text-sm">Compliance</Link>
              <Link to="/workflows" className="text-sm">Workflows</Link>
            </>
          )}
        </div>
        <div>
          {!user ? (
            <Link to="/login" className="text-sm text-blue-600">Login</Link>
          ) : (
            <button className="text-sm text-red-600" onClick={() => { logout(); navigate('/login') }}>Logout</button>
          )}
        </div>
      </div>
    </nav>
  )
}