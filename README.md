# personalized_paper_explorer

cat > README.md << 'EOF'
# Personalized Research Paper Explorer (RAG + Citation Graph)

Ask research questions over arXiv papers and get grounded answers with citations. 
Features:
- Hybrid retrieval (BM25 + vectors + RRF)
- RAG answers with inline source anchors [S1], [S2]
- Paper comparison tables (Markdown)
- Citation graph (Neo4j)
- Fully open-source stack (FastAPI, Chroma, Ollama, Next.js, Neo4j)

## Quick start
```bash
docker compose up -d --build
# open http://localhost:3000
