from typing import Dict, List
import time, requests, chromadb
from .config import PERSIST_DIR, OLLAMA_BASE_URL, LLM_MODEL, TOP_K
from .search import hybrid_search
from .prompts import SYSTEM_PROMPT, USER_PROMPT

def fetch_docs(ids: List[str]):
    col = chromadb.PersistentClient(path=PERSIST_DIR).get_collection("papers")
    # Do NOT request "ids" in include; Chroma returns ids automatically
    return col.get(ids=ids, include=["documents", "metadatas"])

def format_context(res) -> str:
    lines=[]
    # ids are always present in response
    for i,_id in enumerate(res["ids"]):
        m = res["metadatas"][i]
        snippet = (res["documents"][i] or "")[:1200].replace("\n"," ")
        lines.append(f"[S{i+1}] {_id} :: {m.get('title','?')} :: {m.get('section','?')} :: {snippet}")
    return "\n\n".join(lines)

def wait_for_ollama(timeout_s: int = 60):
    t0 = time.time()
    while time.time() - t0 < timeout_s:
        try:
            r = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=3)
            if r.ok:
                return True
        except requests.RequestException:
            pass
        time.sleep(1)
    return False

def ollama_chat(system: str, user: str) -> str:
    if not wait_for_ollama(60):
        raise RuntimeError("LLM runtime (Ollama) is not reachable. Check the ollama container and model pulls.")
    r = requests.post(f"{OLLAMA_BASE_URL}/api/chat", json={
        "model": LLM_MODEL,
        "messages":[{"role":"system","content":system},{"role":"user","content":user}],
        "options":{"temperature":0.2,"num_ctx":8192}
    }, timeout=180)
    if not r.ok:
        try:
            err = r.json()
        except Exception:
            err = {"error": r.text}
        raise RuntimeError(f"Ollama error: {err}")
    data = r.json()
    if "message" not in data or "content" not in data["message"]:
        raise RuntimeError(f"Unexpected Ollama response: {data}")
    return data["message"]["content"]

def rag_answer(query: str, top_k: int = TOP_K) -> Dict:
    ids = hybrid_search(query, top_k=top_k)
    if not ids:
        return {"answer": "I couldn't retrieve any relevant chunks yet. Try ingesting papers first.", "sources": []}
    res = fetch_docs(ids)
    ctx = format_context(res)
    out = ollama_chat(SYSTEM_PROMPT, USER_PROMPT.format(query=query, context=ctx))
    sources=[{"anchor":f"S{i+1}","doc_id":res["ids"][i],
              "title":res["metadatas"][i].get("title",""),
              "url":res["metadatas"][i].get("url",""),
              "section":res["metadatas"][i].get("section","")} for i in range(len(res["ids"]))]
    return {"answer": out, "sources": sources}
