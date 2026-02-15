'use client';

import { useState } from 'react';
import { API_BASE } from '../../lib/api';

export default function BacktestPage() {
  const [ticker, setTicker] = useState('SHOP.TO');
  const [result, setResult] = useState<any>(null);

  async function run() {
    const r = await fetch(`${API_BASE}/api/backtest`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ticker, lookback_years: 3, fee_bps: 10, slippage_bps: 10 })
    });
    setResult(await r.json());
  }

  return (
    <main>
      <h2>Backtest</h2>
      <p><b>Not financial advice.</b></p>
      <input value={ticker} onChange={(e) => setTicker(e.target.value)} />
      <button onClick={run}>Run Backtest</button>
      <pre>{JSON.stringify(result, null, 2)}</pre>
    </main>
  );
}
