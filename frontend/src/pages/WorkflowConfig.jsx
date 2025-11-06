import { useEffect, useState } from 'react'
import api from '../api/client'
import Card from '../components/ui/Card'
import Button from '../components/ui/Button'
import Input from '../components/ui/Input'

export default function WorkflowConfig() {
  const [config, setConfig] = useState({ role_order: ['L1', 'L2', 'L3'] })
  const [requestId, setRequestId] = useState('REQ-001')
  const [status, setStatus] = useState(null)

  const load = async () => {
    const res = await api.get('/api/v1/workflows/config')
    setConfig(res.data)
  }

  useEffect(() => { load() }, [])

  const save = async () => {
    const res = await api.post('/api/v1/workflows/config', config)
    setConfig(res.data)
  }

  const createReq = async () => {
    const res = await api.post('/api/v1/workflows/requests', { request_id: requestId, title: 'Demo', current_stage_index: 0 })
    setStatus(res.data)
  }

  const transition = async (action) => {
    const res = await api.post('/api/v1/workflows/transition', { request_id: requestId, action })
    setStatus(res.data)
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      <Card>
        <h3 className="font-semibold mb-2">Config</h3>
        <Input value={config.role_order.join(',')} onChange={e => setConfig({ role_order: e.target.value.split(',').map(s => s.trim()) })} />
        <Button className="mt-3" onClick={save}>Save</Button>
      </Card>
      <Card>
        <h3 className="font-semibold mb-2">Requests</h3>
        <Input value={requestId} onChange={e => setRequestId(e.target.value)} />
        <div className="flex gap-2 mt-3">
          <Button onClick={createReq}>Create</Button>
          <Button className="bg-green-600 hover:bg-green-700" onClick={() => transition('approve')}>Approve</Button>
          <Button className="bg-yellow-600 hover:bg-yellow-700" onClick={() => transition('reject')}>Reject</Button>
        </div>
        {status && (
          <div className="mt-3 text-sm">Status: {status.status} {status.stage ? `(Stage ${status.stage})` : ''}</div>
        )}
      </Card>
    </div>
  )
}