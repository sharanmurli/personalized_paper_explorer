from typing import Optional, Dict
from semanticscholar import SemanticScholar
from .config import SEMANTIC_SCHOLAR_API_KEY

def enrich_with_semanticscholar(arxiv_id: str) -> Optional[Dict]:
    try:
        s2 = SemanticScholar(api_key=SEMANTIC_SCHOLAR_API_KEY or None)
        return s2.get_paper(f"ARXIV:{arxiv_id}", fields=[
            "title","authors","year","url","references.title","references.externalIds"
        ])
    except Exception:
        return None
