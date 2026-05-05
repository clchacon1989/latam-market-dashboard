import { useState, useEffect } from 'react'

const API = 'http://localhost:8000'

function useApi(url) {
  const [data, setData] = useState(null)
  useEffect(() => {
    fetch(API + url).then(r => r.json()).then(setData).catch(console.error)
  }, [url])
  return data
}

export default function App() {
  const stats = useApi('/api/stats')
  const articles = useApi('/api/articles')
  const summaries = useApi('/api/summaries')

  return (
    <div style={{fontFamily: 'Arial', maxWidth: '1100px', margin: '0 auto', padding: '24px'}}>
      <div style={{background: '#1e3a5f', color: 'white', padding: '24px', borderRadius: '12px', marginBottom: '24px'}}>
        <h1 style={{margin: 0}}>LATAM Market Intelligence</h1>
        <p style={{margin: '8px 0 0', color: '#93c5fd'}}>Real-time startup insights across Latin America</p>
      </div>
      {stats && (
        <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(130px, 1fr))', gap: '12px', marginBottom: '24px'}}>
          {stats.map(s => (
            <div key={s.country} style={{background: 'white', border: '1px solid #e2e8f0', borderRadius: '10px', padding: '16px', textAlign: 'center'}}>
              <div style={{fontSize: '28px', fontWeight: 'bold', color: '#2563eb'}}>{s.article_count}</div>
              <div style={{fontSize: '13px', color: '#64748b'}}>{s.country}</div>
            </div>
          ))}
        </div>
      )}
      <div style={{background: 'white', border: '1px solid #e2e8f0', borderRadius: '12px', padding: '24px', marginBottom: '24px'}}>
        <h2 style={{margin: '0 0 16px', color: '#7c3aed'}}>AI Market Summaries — Powered by Claude</h2>
        {!summaries || summaries.length === 0
          ? <p style={{color: '#94a3b8'}}>No summaries yet.</p>
          : summaries.slice(0, 3).map(s => (
            <div key={s.id} style={{borderLeft: '4px solid #7c3aed', paddingLeft: '16px', marginBottom: '20px'}}>
              <div style={{display: 'flex', gap: '8px', marginBottom: '8px'}}>
                <span style={{background: '#dbeafe', color: '#1d4ed8', padding: '2px 8px', borderRadius: '4px', fontSize: '12px'}}>{s.country}</span>
                <span style={{background: '#dcfce7', color: '#166534', padding: '2px 8px', borderRadius: '4px', fontSize: '12px'}}>{s.industry}</span>
              </div>
              <p style={{fontSize: '14px', lineHeight: '1.7', color: '#374151'}}>{s.summary}</p>
            </div>
          ))
        }
      </div>
      <div style={{background: 'white', border: '1px solid #e2e8f0', borderRadius: '12px', padding: '24px'}}>
        <h2 style={{margin: '0 0 16px'}}>Latest News</h2>
        {!articles || articles.length === 0
          ? <p style={{color: '#94a3b8'}}>Loading...</p>
          : articles.slice(0, 20).map(a => (
            <div key={a.id} style={{padding: '10px 0', borderBottom: '1px solid #f1f5f9'}}>
              <a href={a.url} target="_blank" rel="noopener noreferrer" style={{color: '#1e293b', fontWeight: '500', fontSize: '14px', textDecoration: 'none'}}>{a.title}</a>
              <div style={{marginTop: '4px', display: 'flex', gap: '6px'}}>
                <span style={{fontSize: '12px', color: '#94a3b8'}}>{a.source}</span>
                <span style={{fontSize: '12px', background: '#f1f5f9', padding: '0 6px', borderRadius: '4px'}}>{a.country}</span>
                <span style={{fontSize: '12px', background: '#f1f5f9', padding: '0 6px', borderRadius: '4px'}}>{a.industry}</span>
              </div>
            </div>
          ))
        }
      </div>
    </div>
  )
}
