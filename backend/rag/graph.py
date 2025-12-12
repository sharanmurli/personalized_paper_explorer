# backend/rag/graph.py
from typing import Dict, List
from py2neo import Graph
from .config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

def g():
    return Graph(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def write_papers_and_edges(papers: List[Dict], refs: Dict[str, List[Dict]]):
    graph = g()
    tx = graph.begin()
    for p in papers:
        tx.run(
            """
            MERGE (p:Paper {id:$id})
            ON CREATE SET p.title=$title, p.year=$year
            ON MATCH  SET p.title=coalesce(p.title,$title), p.year=coalesce(p.year,$year)
            """,
            id=p["paper_id"], title=p["title"], year=int(p.get("year", 0) or 0)
        )
    for pid, rlist in refs.items():
        for r in rlist:
            if "paper_id" in r:
                tx.run(
                    """
                    MERGE (q:Paper {id:$id})
                    ON CREATE SET q.title=$title, q.year=$year
                    """,
                    id=r["paper_id"], title=r.get("title", ""), year=int(r.get("year", 0) or 0)
                )
                tx.run(
                    """
                    MATCH (a:Paper {id:$src}),(b:Paper {id:$dst})
                    MERGE (a)-[:CITES]->(b)
                    """,
                    src=pid, dst=r["paper_id"]
                )
    tx.commit()

def neighbors(pid: str, depth: int = 1):
    depth = max(1, min(int(depth or 1), 5))  # clamp 1..5
    cypher = f"""
    MATCH (p:Paper {{id:$pid}})-[:CITES*1..{depth}]->(q)
    RETURN p.id as src, q.id as dst, q.title as title, q.year as year
    """
    return g().run(cypher, pid=pid).data()
