import { API_BASE } from '../../../lib/api';

async function load(ticker: string) {
  const [chart, ind, news] = await Promise.all([
    fetch(`${API_BASE}/api/symbol/${ticker}/chart`, { cache: 'no-store' }).then((r) => r.json()),
    fetch(`${API_BASE}/api/symbol/${ticker}/indicators`, { cache: 'no-store' }).then((r) => r.json()),
    fetch(`${API_BASE}/api/symbol/${ticker}/news`, { cache: 'no-store' }).then((r) => r.json()),
  ]);
  return { chart, ind, news };
}

export default async function SymbolPage({ params }: { params: { ticker: string } }) {
  const data = await load(params.ticker);
  return (
    <main>
      <h2>{params.ticker} Detail</h2>
      <p><b>Not financial advice.</b></p>
      <p>Score: {data.ind.score}</p>
      <p>Reasons: {(data.ind.reasons || []).join(', ')}</p>
      <h3>News</h3>
      <ul>
        {(data.news.items || []).map((n: any, i: number) => <li key={i}>[{n.tag}] <a href={n.url}>{n.title}</a></li>)}
      </ul>
      <h3>Chart Data Preview (last 5 bars)</h3>
      <pre>{JSON.stringify((data.chart.bars || []).slice(-5), null, 2)}</pre>
    </main>
  );
}
