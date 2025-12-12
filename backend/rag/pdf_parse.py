import fitz
from typing import List, Dict

def extract_text_by_page(pdf_path: str) -> List[str]:
    doc = fitz.open(pdf_path)
    return [p.get_text("text") for p in doc]

def basic_sections(pages: List[str]) -> List[Dict]:
    text = "\n".join(pages); lower=text.lower()
    anchors = ["abstract","introduction","method","methods","experiments","results","discussion","conclusion","references"]
    idx = sorted([(lower.find(a), a) for a in anchors if lower.find(a)!=-1], key=lambda x:x[0])
    if not idx: return [{"section":"full_text","text":text}]
    chunks=[]
    for i,(start,label) in enumerate(idx):
        end = idx[i+1][0] if i+1<len(idx) else len(text)
        chunks.append({"section":label, "text":text[start:end].strip()})
    return chunks
