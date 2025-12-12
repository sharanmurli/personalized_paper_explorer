from typing import List, Dict
import arxiv, os, requests
from .config import DATA_DIR

def search_arxiv(query: str, max_results: int = 20) -> List[Dict]:
    results = arxiv.Search(query=query, max_results=max_results, sort_by=arxiv.SortCriterion.Relevance).results()
    out=[]
    for r in results:
        out.append({
            "arxiv_id": r.entry_id.split("/")[-1],
            "title": r.title, "summary": r.summary,
            "authors": [a.name for a in r.authors],
            "published": r.published.strftime("%Y-%m-%d"),
            "pdf_url": r.pdf_url, "primary_category": r.primary_category, "categories": r.categories
        })
    return out

def download_pdf(pdf_url: str, paper_id: str) -> str:
    os.makedirs(f"{DATA_DIR}/pdfs", exist_ok=True)
    dest = f"{DATA_DIR}/pdfs/{paper_id}.pdf"
    if not os.path.exists(dest):
        r = requests.get(pdf_url, timeout=60)
        r.raise_for_status()
        with open(dest, "wb") as f: f.write(r.content)
    return dest
