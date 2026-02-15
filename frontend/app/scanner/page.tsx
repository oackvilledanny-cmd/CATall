import Link from 'next/link';
import { API_BASE } from '../../lib/api';

async function loadScan() {
  const res = await fetch(`${API_BASE}/api/scan`, { cache: 'no-store' });
  return res.json();
}

export default async function ScannerPage() {
  const data = await loadScan();
  return (
    <main>
      <h2>Scanner Top10</h2>
      <p><b>Not financial advice.</b></p>
      <table border={1} cellPadding={6}>
        <thead><tr><th>Ticker</th><th>Score</th><th>Jump Days</th><th>Reasons</th></tr></thead>
        <tbody>
          {(data.top10 || []).map((r: any) => (
            <tr key={r.ticker}>
              <td><Link href={`/symbol/${r.ticker}`}>{r.ticker}</Link></td>
              <td>{r.score}</td>
              <td>{r.jump_days}</td>
              <td>{(r.reasons || []).join(', ')}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </main>
  );
}
