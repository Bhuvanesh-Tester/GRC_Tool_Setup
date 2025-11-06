import { useEffect, useState } from 'react'
import api from '../api/client'
import Card from '../components/ui/Card'
import Button from '../components/ui/Button'
import Input from '../components/ui/Input'

function badgeColor(score) {
  if (score >= 20) return 'bg-red-600'
  if (score >= 10) return 'bg-yellow-500'
  return 'bg-green-600'
}

export default function Risks() {
  const [items, setItems] = useState([])
  const [title, setTitle] = useState('')
  const [impact, setImpact] = useState(3)
  const [likelihood, setLikelihood] = useState(3)

  const load = async () => {
    const res = await api.get('/api/v1/risks/')
    setItems(res.data.items)
  }

  useEffect(() => { load() }, [])

  const create = async () => {
    await api.post('/api/v1/risks/', { title, impact: Number(impact), likelihood: Number(likelihood) })
    setTitle(''); setImpact(3); setLikelihood(3); await load()
  }

  const remove = async (id) => {
    await api.delete(`/api/v1/risks/${id}`)
    await load()
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      <Card>
        <h3 className="font-semibold mb-2">Create Risk</h3>
        <Input placeholder="Title" value={title} onChange={e => setTitle(e.target.value)} />
        <div className="flex gap-2 mt-2">
          <Input type="number" min="1" max="5" value={impact} onChange={e => setImpact(e.target.value)} />
          <Input type="number" min="1" max="5" value={likelihood} onChange={e => setLikelihood(e.target.value)} />
        </div>
        <Button className="mt-3" onClick={create} disabled={!title}>Create</Button>
      </Card>
      <Card>
        <h3 className="font-semibold mb-2">Risks</h3>
        <ul className="space-y-2">
          {items.map(i => (
            <li key={i.id} className="border rounded p-2 flex items-center justify-between">
              <div>
                <div className="font-medium">{i.title}</div>
                <div className="text-xs text-gray-500">Impact {i.impact} × Likelihood {i.likelihood} = Score {i.score}</div>
              </div>
              <div className="flex gap-2 items-center">
                <span className={`text-white text-xs px-2 py-1 rounded ${badgeColor(i.score)}`}>{i.score >= 20 ? 'High' : i.score >= 10 ? 'Medium' : 'Low'}</span>
                <Button className="bg-red-600 hover:bg-red-700" onClick={() => remove(i.id)}>Delete</Button>
              </div>
            </li>
          ))}
        </ul>
      </Card>
    </div>
  )
}