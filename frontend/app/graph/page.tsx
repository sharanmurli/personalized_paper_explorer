"use client";
import dynamic from "next/dynamic";
import { useEffect, useState } from "react";
const CytoscapeComponent = dynamic(() => import("react-cytoscapejs"), { ssr: false });

export default function GraphPage() {
  const [pid, setPid] = useState("ARXIV:2401.00001");
  const [elements, setElements] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const load = async () => {
    try {
      setLoading(true);
      const r = await fetch(`/api/graph/neighbors?pid=${encodeURIComponent(pid)}&depth=1`);
      if (!r.ok) throw new Error(`Graph failed: ${r.status}`);
      const data = await r.json();
      const nodes: any = {};
      const edges: any[] = [];
      nodes[pid] = { data: { id: pid, label: pid } };
      data.edges.forEach((e: any) => {
        nodes[e.dst] = nodes[e.dst] || { data: { id: e.dst, label: e.title || e.dst } };
        edges.push({ data: { source: pid, target: e.dst } });
      });
      setElements([...Object.values(nodes), ...edges]);
    } catch (e) {
      alert(String(e));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <main className="p-6" style={{ maxWidth: 1100, margin: "0 auto" }}>
      <h1 style={{ fontSize: 24, fontWeight: 700, marginBottom: 12 }}>Citation Graph</h1>
      <div style={{ display: "flex", gap: 8, marginBottom: 12 }}>
        <input
          value={pid}
          onChange={(e) => setPid(e.target.value)}
          style={{ flex: 1, padding: "8px", border: "1px solid #ccc", borderRadius: 6 }}
        />
        <button onClick={load} disabled={loading} style={{ padding: "8px 12px" }}>
          {loading ? "..." : "Load"}
        </button>
      </div>
      <CytoscapeComponent elements={elements} style={{ width: "100%", height: "600px", border: "1px solid #ddd" }} />
    </main>
  );
}
