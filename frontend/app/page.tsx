import Link from 'next/link';

export default function Home() {
  return (
    <main>
      <ul>
        <li><Link href="/login">Login</Link></li>
        <li><Link href="/scanner">Scanner</Link></li>
        <li><Link href="/portfolio">Portfolio Builder</Link></li>
        <li><Link href="/backtest">Backtest</Link></li>
      </ul>
    </main>
  );
}
