import { useEffect, useState } from 'react'
import api from '../api/client'
import Card from '../components/ui/Card'
import Button from '../components/ui/Button'
import Input from '../components/ui/Input'

export default function Policies() {
  const [items, setItems] = useState([])
  const [title, setTitle] = useState('')
  const [desc, setDesc] = useState('')
  const [file, setFile] = useState(null)

  const load = async () => {
    const res = await api.get('/api/v1/policies/')
    setItems(res.data.items)
  }

  useEffect(() => { load() }, [])

  const create = async () => {
    const res = await api.post('/api/v1/policies/', { title, description: desc })
    setTitle(''); setDesc(''); await load()
  }

  const remove = async (id) => {
    await api.delete(`/api/v1/policies/${id}`)
    await load()
  }

  const upload = async (id) => {
    if (!file) return
    const fd = new FormData()
    fd.append('file', file)
    const res = await api.post(`/api/v1/policies/${id}/upload`, fd, { headers: { 'Content-Type': 'multipart/form-data' } })
    await load()
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      <Card>
        <h3 className="font-semibold mb-2">Create Policy</h3>
        <Input placeholder="Title" value={title} onChange={e => setTitle(e.target.value)} />
        <Input className="mt-2" placeholder="Description" value={desc} onChange={e => setDesc(e.target.value)} />
        <Button className="mt-3" onClick={create} disabled={!title}>Create</Button>
      </Card>
      <Card>
        <h3 className="font-semibold mb-2">Policies</h3>
        <input type="file" className="mb-2" onChange={e => setFile(e.target.files[0])} />
        <ul className="space-y-2">
          {items.map(i => (
            <li key={i.id} className="border rounded p-2 flex items-center justify-between">
              <div>
                <div className="font-medium">{i.title} <span className="text-xs text-gray-500">({i.status})</span></div>
                {i.file_url && <a className="text-xs text-blue-600" href={i.file_url} target="_blank">File</a>}
              </div>
              <div className="flex gap-2">
                <Button className="bg-green-600 hover:bg-green-700" onClick={() => upload(i.id)}>Upload</Button>
                <Button className="bg-red-600 hover:bg-red-700" onClick={() => remove(i.id)}>Delete</Button>
              </div>
            </li>
          ))}
        </ul>
      </Card>
    </div>
  )
}