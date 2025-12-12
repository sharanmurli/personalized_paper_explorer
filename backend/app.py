from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from rag.ingest_arxiv import search_arxiv, download_pdf
from rag.ingest_semanticscholar import enrich_with_semanticscholar
from rag.pdf_parse import extract_text_by_page, basic_sections
from rag.index import chunk_and_embed
from rag.search import hybrid_search
from rag.chat import rag_answer
from rag.graph import write_papers_and_edges, neighbors

# ADD these imports at the top:
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(title="Personalized Research Paper Explorer")



# ADD this block right after app = FastAPI(...)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class IngestRequest(BaseModel):
    query: str
    max_results: int = 10

@app.get("/search_arxiv")
def search_arxiv_api(q: str, k: int = 10):
    return search_arxiv(q, max_results=k)

@app.post("/ingest")
def ingest(req: IngestRequest):
    metas = search_arxiv(req.query, req.max_results)
    papers=[]; refs={}
    total=0
    for m in metas:
        pid = m["arxiv_id"]
        pdf = download_pdf(m["pdf_url"], pid)
        pages = extract_text_by_page(pdf)
        sections = basic_sections(pages)
        s2 = enrich_with_semanticscholar(pid)
        url = (s2.url if s2 and hasattr(s2,"url") else m["pdf_url"])
        meta = {"paper_id": f"ARXIV:{pid}", "title": m["title"], "authors": m["authors"],
                "year": (s2.year if s2 else m["published"][:4]), "arxiv_id": pid, "url": url}
        total += chunk_and_embed(meta, sections)
        papers.append(meta)
        rlist=[]
        if s2 and hasattr(s2,"references"):
            for r in s2.references:
                rid = (r.externalIds.get("ArXiv") if r.externalIds else None)
                if rid: rlist.append({"paper_id": f"ARXIV:{rid}", "title": r.title, "year": r.get("year",None)})
        refs[meta["paper_id"]] = rlist
    write_papers_and_edges(papers, refs)
    return {"indexed_chunks": total, "papers": [p["paper_id"] for p in papers]}

@app.get("/search")
def search(q: str, k: int = 6):
    return {"ids": hybrid_search(q, top_k=k)}

class ChatRequest(BaseModel):
    query: str
    k: int = 6

@app.post("/chat")
def chat(req: ChatRequest):
    return rag_answer(req.query, top_k=req.k)

@app.get("/graph/neighbors")
def graph_neighbors(pid: str, depth: int = 1):
    return {"edges": neighbors(pid, depth=depth)}
