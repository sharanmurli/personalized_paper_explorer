# backend/rag/index.py
from typing import List, Dict
import chromadb
from sentence_transformers import SentenceTransformer
from llama_index.core.node_parser import SentenceSplitter
from .config import PERSIST_DIR, CHUNK_SIZE, CHUNK_OVERLAP

def get_chroma():
    client = chromadb.PersistentClient(path=PERSIST_DIR)
    return client.get_or_create_collection("papers", metadata={"hnsw:space": "cosine"})

def chunk_and_embed(paper_meta: Dict, sections: List[Dict]) -> int:
    splitter = SentenceSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    docs, metas, ids = [], [], []
    for i, sec in enumerate(sections):
        for j, ch in enumerate(splitter.split_text(sec["text"])):
            docs.append(ch)
            metas.append({
                "paper_id": paper_meta["paper_id"],
                "title": paper_meta["title"],
                "authors": ", ".join(paper_meta.get("authors", [])),
                "section": sec["section"],
                "year": paper_meta.get("year", ""),
                "arxiv_id": paper_meta.get("arxiv_id", ""),
                "url": paper_meta.get("url", "")
            })
            ids.append(f'{paper_meta["paper_id"]}:{i}:{j}')

    # 👉 Convert to list-of-lists for Chroma
    embedder = SentenceTransformer("BAAI/bge-base-en-v1.5")
    vecs = embedder.encode(docs, convert_to_numpy=True, normalize_embeddings=True).tolist()

    get_chroma().upsert(ids=ids, documents=docs, embeddings=vecs, metadatas=metas)
    return len(ids)
