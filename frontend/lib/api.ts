export const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';

export async function getScan() {
  const r = await fetch(`${API_BASE}/api/scan`, { cache: 'no-store' });
  return r.json();
}
