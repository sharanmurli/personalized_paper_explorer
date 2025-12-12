# backend/rag/search.py
from typing import List
import numpy as np, chromadb
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer
from .config import PERSIST_DIR, TOP_K

def reciprocal_rank_fusion(rank_lists: List[List[str]], k: int = 60) -> List[str]:
    scores = {}
    for rl in rank_lists:
        for rank, doc_id in enumerate(rl, start=1):
            scores[doc_id] = scores.get(doc_id, 0.0) + 1.0 / (k + rank)
    return [d for d, _ in sorted(scores.items(), key=lambda x: x[1], reverse=True)]

def chroma_top_ids(query: str, top_k: int) -> List[str]:
    col = chromadb.PersistentClient(path=PERSIST_DIR).get_collection("papers")
    embedder = SentenceTransformer("BAAI/bge-base-en-v1.5")
    qv = embedder.encode([query], convert_to_numpy=True, normalize_embeddings=True)[0].tolist()  # Chroma expects list
    res = col.query(query_embeddings=[qv], n_results=top_k)
    # ids are always present in the response
    return (res.get("ids") or [[]])[0] if res and res.get("ids") else []

def bm25_top_ids(query: str, top_k: int) -> List[str]:
    col = chromadb.PersistentClient(path=PERSIST_DIR).get_collection("papers")
    # ✅ do NOT request "ids" in include; Chroma always returns ids
    res = col.get(include=["documents"])
    docs = res.get("documents") or []
    ids = res.get("ids") or []
    if not docs or not ids:
        return []
    bm = BM25Okapi([d.split() for d in docs])
    scores = bm.get_scores(query.split())
    idx = np.argsort(scores)[::-1][:top_k]
    return [ids[i] for i in idx]

def hybrid_search(query: str, top_k: int = TOP_K) -> List[str]:
    v = chroma_top_ids(query, top_k * 2) or []
    b = bm25_top_ids(query, top_k * 2) or []
    if not v and not b:
        return []
    fused = reciprocal_rank_fusion([v, b])
    return fused[:top_k]
