import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const LANGUAGES = [
  { code: 'en', flag: '🇺🇸' }, { code: 'de', flag: '🇩🇪' }, { code: 'zh', flag: '🇨🇳' }, { code: 'jp', flag: '🇯🇵' }
];

const HUB_LOCATIONS = ["Central Hub (Frankfurt)", "East Hub (Tokyo)", "West Hub (Chicago)", "South Hub (Mumbai)"];

// ── Icons ──────────────────────────────────────────────────────────────────
const Icons = {
  Scan: "🔍", Global: "🌐", Archive: "⏳", Settings: "⚙️", 
  Check: "✅", Warning: "⚠️", Play: "▶️", Download: "📄",
  Bell: "🔔", Shield: "🛡️", Terminal: "📟", User: "👤",
  Group: "📁", List: "📋", Print: "🖨️", Search: "🔎"
};

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [viewMode, setViewMode] = useState('grouped'); 
  const [lang, setLang] = useState('en');
  const [hub, setHub] = useState(HUB_LOCATIONS[0]);
  const [searchTerm, setSearchTerm] = useState('');
  
  // Batch & History State
  const [batch, setBatch] = useState([]);
  const [isAnalyzingAll, setIsAnalyzingAll] = useState(false);
  const [history, setHistory] = useState(() => {
    const saved = localStorage.getItem('steel_vision_enterprise_v3');
    return saved ? JSON.parse(saved) : [];
  });
  
  const [isOnline, setIsOnline] = useState(false);
  const fileInputRef = useRef();

  useEffect(() => {
    localStorage.setItem('steel_vision_enterprise_v3', JSON.stringify(history));
  }, [history]);

  useEffect(() => {
    const checkHealth = () => {
      axios.get(`${API_BASE}/health`).then(() => setIsOnline(true)).catch(() => setIsOnline(false));
    };
    checkHealth();
    const timer = setInterval(checkHealth, 30000);
    return () => clearInterval(timer);
  }, []);

  // ── Actions ──────────────────────────────────────────────────────────────
  const analyzeSingle = async (id) => {
    const item = batch.find(b => b.id === id);
    if (!item || item.result || item.loading) return;
    setBatch(prev => prev.map(b => b.id === id ? { ...b, loading: true } : b));
    const fd = new FormData();
    fd.append('image', item.file);
    try {
      const res = await axios.post(`${API_BASE}/predict`, fd);
      const data = res.data;
      setBatch(prev => prev.map(b => b.id === id ? { ...b, loading: false, result: data } : b));
      setHistory(prev => [{
        id: Date.now() + Math.random(),
        defect: data.defect,
        confidence: data.confidence,
        thumb: item.preview,
        time: new Date().toISOString(),
        name: item.name
      }, ...prev].slice(0, 100));
    } catch (err) {
      setBatch(prev => prev.map(b => b.id === id ? { ...b, loading: false } : b));
    }
  };

  const analyzeAll = async () => {
    setIsAnalyzingAll(true);
    for (const item of batch) {
      if (!item.result) await analyzeSingle(item.id);
    }
    setIsAnalyzingAll(false);
    setViewMode('grouped');
  };

  const getGroupedBatch = () => {
    const groups = {};
    batch.forEach(item => {
      const key = item.result ? item.result.defect : 'Awaiting Analysis';
      if (!groups[key]) groups[key] = [];
      groups[key].push(item);
    });
    return groups;
  };

  // ── Filters ──────────────────────────────────────────────────────────────
  const filteredHistory = history.filter(h => 
    h.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    h.defect.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="app-layout">
      <aside className="sidebar no-print">
        <div className="brand"><div className="brand-icon">S</div> STEEL VISION <span style={{fontWeight: 400}}>GRANDMASTER</span></div>
        <div className="nav-group">
          <div className="nav-label">Operations Center</div>
          <div className={`nav-item ${activeTab === 'dashboard' ? 'active' : ''}`} onClick={() => setActiveTab('dashboard')}>
            <span>{Icons.Scan}</span> Batch Inspection
          </div>
          <div className={`nav-item ${activeTab === 'archive' ? 'active' : ''}`} onClick={() => setActiveTab('archive')}>
            <span>{Icons.Archive}</span> Global History
          </div>
        </div>
        <div className="nav-group">
          <div className="nav-label">Industrial Node</div>
          <div className="nav-item"><span>{Icons.Global}</span> Frankfurt Central</div>
        </div>
      </aside>

      <main className="main-area">
        <header className="top-header no-print">
           <div className="card-title">Production Terminal // Grandmaster Edition</div>
           <div style={{ display: 'flex', gap: '20px', alignItems: 'center' }}>
              <div className="status-indicator"><div className={`dot ${isOnline ? 'dot-online' : 'dot-offline'}`} /> {isOnline ? 'STABLE' : 'OFFLINE'}</div>
              <div style={{ display: 'flex', gap: '8px' }}>
                {LANGUAGES.map(l => <button key={l.code} onClick={() => setLang(l.code)} style={{ background: lang === l.code ? 'var(--primary-soft)' : 'transparent', border: 'none', color: 'white', cursor: 'pointer', padding: '6px' }}>{l.flag}</button>)}
              </div>
           </div>
        </header>

        <div className="content-wrapper">
          {activeTab === 'dashboard' && (
            <div className="dashboard-grid" style={{ display: 'block' }}>
              <div className="card">
                <div className="card-header no-print">
                  <h3 className="card-title">Neural Ingestion Pipeline ({batch.length})</h3>
                  <div style={{ display: 'flex', gap: '10px' }}>
                    <div style={{ display: 'flex', background: 'var(--bg-app)', padding: '2px', borderRadius: '8px' }}>
                       <button className="btn" style={{ background: viewMode === 'list' ? 'var(--border)' : 'transparent' }} onClick={() => setViewMode('list')}>{Icons.List}</button>
                       <button className="btn" style={{ background: viewMode === 'grouped' ? 'var(--border)' : 'transparent' }} onClick={() => setViewMode('grouped')}>{Icons.Group}</button>
                    </div>
                    <button className="btn btn-secondary" onClick={() => fileInputRef.current.click()}>+ Import</button>
                    <button className="btn btn-primary" onClick={analyzeAll} disabled={isAnalyzingAll || batch.length === 0}>
                       {isAnalyzingAll ? "Fine-Tuning Predictions..." : "Grandmaster Scan"}
                    </button>
                    {batch.filter(b => b.result).length > 0 && (
                      <button className="btn btn-secondary" onClick={() => window.print()}>{Icons.Print} Report</button>
                    )}
                  </div>
                </div>

                {viewMode === 'list' ? (
                  <div className="data-list">
                    {batch.map(item => (
                      <div key={item.id} className="card" style={{ padding: '12px', marginBottom: '8px' }}>
                        <div style={{ display: 'flex', gap: '20px', alignItems: 'center' }}>
                          <img src={item.preview} style={{ width: '80px', height: '50px', objectFit: 'cover', borderRadius: '4px' }} alt="S" />
                          <div style={{ flex: 1 }}>
                             <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>{item.name}</div>
                             {item.result ? <b style={{ color: 'var(--primary)', textTransform: 'uppercase' }}>{item.result.defect}</b> : 'Awaiting...'}
                          </div>
                          {item.result && (
                            <div style={{ textAlign: 'right' }}>
                               <div style={{ fontSize: '0.9rem', fontWeight: 800 }}>{(item.result.confidence * 100).toFixed(1)}%</div>
                            </div>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '32px' }}>
                    {Object.entries(getGroupedBatch()).map(([group, items]) => (
                      <div key={group}>
                        <div style={{ fontSize: '0.8rem', fontWeight: 800, color: 'var(--primary)', borderBottom: '1px solid var(--border)', paddingBottom: '8px', marginBottom: '16px', textTransform: 'uppercase' }}>
                           {group.replace(/_/g, ' ')} ({items.length} Samples)
                        </div>
                        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(180px, 1fr))', gap: '20px' }}>
                          {items.map(item => (
                            <div key={item.id} style={{ position: 'relative', border: '1px solid var(--border)', borderRadius: '8px', overflow: 'hidden', background: 'var(--bg-card)' }}>
                               <img src={item.preview} style={{ width: '100%', height: '110px', objectFit: 'cover' }} alt="S" />
                               <div style={{ padding: '10px' }}>
                                  <div style={{ fontSize: '0.65rem', color: 'var(--text-secondary)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }} title={item.name}>
                                    {item.name}
                                  </div>
                                  {item.result && (
                                    <div style={{ fontSize: '0.75rem', fontWeight: 700, marginTop: '4px' }}>
                                       {Math.round(item.result.confidence * 100)}% Confidence
                                    </div>
                                  )}
                               </div>
                               {item.result && item.result.confidence < 0.75 && (
                                 <div style={{ position: 'absolute', top: 8, left: 8, background: 'var(--warning)', color: 'black', padding: '2px 8px', borderRadius: '4px', fontSize: '0.6rem', fontWeight: 800 }}>
                                    VERIFY
                                 </div>
                               )}
                            </div>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
                {batch.length === 0 && <div className="dropzone" onClick={() => fileInputRef.current.click()}>🚀 Upload Industrial Batch to Initialize</div>}
                <input type="file" ref={fileInputRef} multiple onChange={(e) => setBatch(prev => [...Array.from(e.target.files).map(f => ({ file: f, preview: URL.createObjectURL(f), result: null, loading: false, id: Math.random(), name: f.name })), ...prev])} hidden />
              </div>
            </div>
          )}

          {activeTab === 'archive' && (
            <div className="card">
               <div className="card-header">
                  <h3 className="card-title">Historical Inspection Vault</h3>
                  <div style={{ position: 'relative', width: '300px' }}>
                    <span style={{ position: 'absolute', left: '10px', top: '10px', color: 'var(--text-muted)' }}>{Icons.Search}</span>
                    <input 
                      type="text" 
                      placeholder="Search by Filename or Defect..." 
                      value={searchTerm}
                      onChange={e => setSearchTerm(e.target.value)}
                      style={{ width: '100%', padding: '10px 10px 10px 35px', background: 'var(--bg-app)', border: '1px solid var(--border)', borderRadius: '8px', color: 'white' }}
                    />
                  </div>
               </div>
               <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))', gap: '20px', marginTop: '20px' }}>
                  {filteredHistory.map(item => (
                    <div key={item.id} className="card" style={{ padding: '0', overflow: 'hidden' }}>
                       <img src={item.thumb} style={{ width: '100%', height: '140px', objectFit: 'cover' }} alt="T" />
                       <div style={{ padding: '16px' }}>
                          <div style={{ fontSize: '0.65rem', color: 'var(--text-muted)', marginBottom: '4px', textOverflow: 'ellipsis', overflow: 'hidden', whiteSpace: 'nowrap' }}>{item.name}</div>
                          <div style={{ fontSize: '0.9rem', fontWeight: 800, color: 'var(--primary)' }}>{item.defect.toUpperCase()}</div>
                          <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>{new Date(item.time).toLocaleString()}</div>
                       </div>
                    </div>
                  ))}
                  {filteredHistory.length === 0 && <div style={{ padding: '100px', textAlign: 'center', gridColumn: '1/-1', color: 'var(--text-muted)' }}>No localized matches found.</div>}
               </div>
            </div>
          )}
        </div>
      </main>

      <style>{`
        @media print {
          .no-print { display: none !important; }
          .app-layout { display: block !important; height: auto !important; background: white !important; color: black !important; }
          .card { background: white !important; border: 1px solid #ddd !important; box-shadow: none !important; color: black !important; page-break-inside: avoid; }
        }
      `}</style>
    </div>
  );
}