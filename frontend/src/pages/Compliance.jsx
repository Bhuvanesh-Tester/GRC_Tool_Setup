import { useEffect, useState } from 'react'
import api from '../api/client'
import Card from '../components/ui/Card'
import Button from '../components/ui/Button'
import Input from '../components/ui/Input'

export default function Compliance() {
  const [items, setItems] = useState([])
  const [name, setName] = useState('')
  const [desc, setDesc] = useState('')

  const load = async () => {
    const res = await api.get('/api/v1/compliance/frameworks')
    setItems(res.data.items)
  }

  useEffect(() => { load() }, [])

  const create = async () => {
    await api.post('/api/v1/compliance/frameworks', { name, description: desc, controls: [] })
    setName(''); setDesc(''); await load()
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      <Card>
        <h3 className="font-semibold mb-2">Create Framework</h3>
        <Input placeholder="Name" value={name} onChange={e => setName(e.target.value)} />
        <Input className="mt-2" placeholder="Description" value={desc} onChange={e => setDesc(e.target.value)} />
        <Button className="mt-3" onClick={create} disabled={!name}>Create</Button>
      </Card>
      <Card>
        <h3 className="font-semibold mb-2">Frameworks</h3>
        <ul className="space-y-2">
          {items.map(i => (
            <li key={i.id} className="border rounded p-2">
              <div className="font-medium">{i.name}</div>
              <div className="text-xs text-gray-500">Controls: {i.controls?.length || 0}</div>
            </li>
          ))}
        </ul>
      </Card>
    </div>
  )
}