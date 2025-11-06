import { Routes, Route, Navigate } from 'react-router-dom'
import Navbar from './components/Navbar'
import Dashboard from './pages/Dashboard'
import Policies from './pages/Policies'
import Risks from './pages/Risks'
import Compliance from './pages/Compliance'
import WorkflowConfig from './pages/WorkflowConfig'
import Login from './pages/Login'

export default function App() {
  return (
    <div className="min-h-screen bg-gray-50 text-gray-900">
      <Navbar />
      <div className="container mx-auto px-4 py-6">
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={<Dashboard />} />
          <Route path="/policies" element={<Policies />} />
          <Route path="/risks" element={<Risks />} />
          <Route path="/compliance" element={<Compliance />} />
          <Route path="/workflows" element={<WorkflowConfig />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </div>
  )
}