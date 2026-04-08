import { useState } from 'react'
import ComparisonForm from './ComparisonForm'

export default function App() {
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  async function handleSubmit(inputs) {
    setError(null)
    setResult(null)
    try {
      const res = await fetch('/api/comparison', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(inputs),
      })
      if (!res.ok) throw new Error(`Server error: ${res.status}`)
      setResult(await res.json())
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div style={{ maxWidth: 600, margin: '40px auto', fontFamily: 'sans-serif' }}>
      <h1>Home Cost Comparison</h1>
      <ComparisonForm onSubmit={handleSubmit} />
      {error && (
        <p style={{ color: 'red', marginTop: 16 }}>Error: {error}</p>
      )}
      {result && (
        <div style={{ marginTop: 24, padding: 16, border: '1px solid #ccc', borderRadius: 4 }}>
          <h2>Result</h2>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  )
}
