"use client";
import { useState } from "react";

export default function Chat() {
  const [q, setQ] = useState("");
  const [answer, setAnswer] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const ask = async () => {
    try {
      setLoading(true);
      const r = await fetch(`/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: q, k: 6 }),
      });
      if (!r.ok) throw new Error(`Chat failed: ${r.status}`);
      const data = await r.json();
      setAnswer(data);
    } catch (e) {
      alert(String(e));
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="p-6" style={{ maxWidth: 900, margin: "0 auto" }}>
      <h1 style={{ fontSize: 24, fontWeight: 700, marginBottom: 12 }}>Ask the Corpus</h1>
      <div style={{ display: "flex", gap: 8, marginBottom: 12 }}>
        <input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="Your question..."
          style={{ flex: 1, padding: "8px", border: "1px solid #ccc", borderRadius: 6 }}
        />
        <button onClick={ask} disabled={loading} style={{ padding: "8px 12px" }}>
          {loading ? "..." : "Ask"}
        </button>
      </div>
      {answer && (
        <div style={{ display: "grid", gap: 16 }}>
          <pre style={{ whiteSpace: "pre-wrap", border: "1px solid #eee", padding: 12, borderRadius: 8 }}>
            {answer.answer}
          </pre>
          <div>
            <h2 style={{ fontWeight: 600 }}>Sources</h2>
            <ul>
              {answer.sources.map((s: any, i: number) => (
                <li key={i}>
                  [{s.anchor}] {s.title} —{" "}
                  <a href={s.url} target="_blank" rel="noreferrer">
                    {s.url}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </main>
  );
}
