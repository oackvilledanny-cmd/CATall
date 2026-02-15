'use client';

import { useState } from 'react';
import { API_BASE } from '../../lib/api';

export default function PortfolioPage() {
  const [json, setJson] = useState<any>(null);
  const [tickers, setTickers] = useState('SHOP.TO,ENB.TO,SU.TO');

  async function run() {
    const r = await fetch(`${API_BASE}/api/portfolio/weights`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        tickers: tickers.split(',').map((s) => s.trim()),
        method: 'risk_parity',
        risk_profile: { level: 'balanced', max_positions: 5, max_weight_per_asset: 0.35, max_drawdown_limit: 0.2 }
      })
    });
    setJson(await r.json());
  }

  return (
    <main>
      <h2>Portfolio Builder</h2>
      <p><b>Not financial advice.</b></p>
      <input value={tickers} onChange={(e) => setTickers(e.target.value)} style={{ width: '60%' }} />
      <button onClick={run}>Calculate</button>
      <pre>{JSON.stringify(json, null, 2)}</pre>
    </main>
  );
}
