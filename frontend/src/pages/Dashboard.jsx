import { useEffect, useState } from 'react'
import api from '../api/client'
import Card from '../components/ui/Card'

export default function Dashboard() {
  const [metrics, setMetrics] = useState({ policies: 0, risks: 0, frameworks: 0 })

  useEffect(() => {
    const load = async () => {
      const [p, r, c] = await Promise.all([
        api.get('/api/v1/policies/'),
        api.get('/api/v1/risks/'),
        api.get('/api/v1/compliance/frameworks'),
      ])
      setMetrics({ policies: p.data.total, risks: r.data.total, frameworks: c.data.total })
    }
    load()
  }, [])

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      <Card>
        <h3 className="font-semibold">Policies</h3>
        <p className="text-3xl">{metrics.policies}</p>
      </Card>
      <Card>
        <h3 className="font-semibold">Risks</h3>
        <p className="text-3xl">{metrics.risks}</p>
      </Card>
      <Card>
        <h3 className="font-semibold">Frameworks</h3>
        <p className="text-3xl">{metrics.frameworks}</p>
      </Card>
    </div>
  )
}