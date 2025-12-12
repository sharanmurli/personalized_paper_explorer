// app/layout.tsx
import "./styles/global.css";

export const metadata = {
  title: "Personalized Research Paper Explorer",
  description: "RAG + citation graph over arXiv",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body style={{ fontFamily: "system-ui, -apple-system, Segoe UI, Roboto, Arial" }}>
        <nav style={{ padding: "12px 16px", borderBottom: "1px solid #eee", display: "flex", gap: 12 }}>
          <a href="/" style={{ fontWeight: 700 }}>Home</a>
          <a href="/chat">Chat</a>
          <a href="/graph">Graph</a>
        </nav>
        <div style={{ padding: 16 }}>{children}</div>
      </body>
    </html>
  );
}
