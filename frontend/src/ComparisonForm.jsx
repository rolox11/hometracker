import { useState } from 'react'

const defaultValues = {
  home_price: '',
  monthly_rent: '',
  mortgage_rate: '',
  investment_return_rate: '',
}

const fields = [
  { name: 'home_price', label: 'Home Price ($)', placeholder: '400000' },
  { name: 'monthly_rent', label: 'Monthly Rent ($)', placeholder: '2000' },
  { name: 'mortgage_rate', label: 'Mortgage Rate (%)', placeholder: '6.5' },
  { name: 'investment_return_rate', label: 'Investment Return Rate (%)', placeholder: '7.0' },
]

export default function ComparisonForm({ onSubmit }) {
  const [values, setValues] = useState(defaultValues)

  function handleChange(e) {
    setValues((prev) => ({ ...prev, [e.target.name]: e.target.value }))
  }

  function handleSubmit(e) {
    e.preventDefault()
    const parsed = Object.fromEntries(
      Object.entries(values).map(([k, v]) => [k, parseFloat(v)])
    )
    onSubmit(parsed)
  }

  return (
    <form onSubmit={handleSubmit}>
      {fields.map(({ name, label, placeholder }) => (
        <div key={name} style={{ marginBottom: 12 }}>
          <label style={{ display: 'block', marginBottom: 4 }}>{label}</label>
          <input
            type="number"
            name={name}
            value={values[name]}
            onChange={handleChange}
            placeholder={placeholder}
            required
            min="0"
            step="any"
            style={{ width: '100%', padding: '8px', boxSizing: 'border-box' }}
          />
        </div>
      ))}
      <button type="submit" style={{ padding: '10px 24px', cursor: 'pointer' }}>
        Compare
      </button>
    </form>
  )
}
