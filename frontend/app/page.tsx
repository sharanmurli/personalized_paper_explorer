"use client";
import { useState } from "react";

export default function Home() {
  const [q, setQ] = useState("");
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const doSearch = async () => {
    try {
      setLoading(true);
      const r = await fetch(`/api/search_arxiv?q=${encodeURIComponent(q)}&k=10`);
      if (!r.ok) throw new Error(`Search failed: ${r.status}`);
      const data = await r.json();
      setResults(data);
    } catch (e) {
      alert(String(e));
    } finally {
      setLoading(false);
    }
  };

  const doIngest = async () => {
    try {
      setLoading(true);
      const r = await fetch(`/api/ingest`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: q, max_results: 5 }),
      });
      if (!r.ok) throw new Error(`Ingest failed: ${r.status}`);
      await r.json();
      alert("Ingested! Try Chat or Graph.");
    } catch (e) {
      alert(String(e));
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="p-6" style={{ maxWidth: 900, margin: "0 auto" }}>
      <h1 className="text-3xl" style={{ fontWeight: 700, marginBottom: 16 }}>
        Personalized Research Paper Explorer
      </h1>

      <div style={{ display: "flex", gap: 8, marginBottom: 16 }}>
        <input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="e.g., retrieval augmented generation biomedical"
          style={{ flex: 1, padding: "8px", border: "1px solid #ccc", borderRadius: 6 }}
        />
        <button onClick={doSearch} disabled={loading} style={{ padding: "8px 12px" }}>
          {loading ? "..." : "Search"}
        </button>
        <button onClick={doIngest} disabled={loading} style={{ padding: "8px 12px" }}>
          {loading ? "..." : "Ingest"}
        </button>
      </div>

      <ul style={{ display: "grid", gap: 12 }}>
        {results.map((r: any, i: number) => (
          <li key={i} style={{ border: "1px solid #eee", padding: 12, borderRadius: 8 }}>
            <div style={{ fontWeight: 600 }}>{r.title}</div>
            <div style={{ fontSize: 12, color: "#555" }}>
              {r.authors?.join(", ")} • {r.published}
            </div>
            <a href={r.pdf_url} target="_blank" rel="noreferrer">
              PDF
            </a>
          </li>
        ))}
      </ul>
    </main>
  );
}
