export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ko">
      <body style={{ fontFamily: 'Arial', margin: 20 }}>
        <h1>CA Tall Scanner</h1>
        <p><b>Not financial advice.</b> 정보 제공/교육 목적.</p>
        {children}
      </body>
    </html>
  );
}
