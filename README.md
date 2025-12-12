
# **Agentic AI-Based Smart Research Assistant**

An interactive, agentic AI-powered research assistant that enables structured academic exploration through LLM-driven reasoning, automated citation retrieval, and knowledge graph visualization using a node-based workflow interface.

---

## **Overview**

The **Agentic AI-Based Smart Research Assistant** is designed to help researchers explore academic topics through transparent, multi-step reasoning workflows. Instead of treating research queries as single-shot prompts, the system models research as an iterative process involving summarization, citation grounding, and visual relationship discovery.

The project combines **LangGraph** for backend workflow orchestration with **ComfyUI** for a visual, node-based frontend, enabling explainable and reusable research pipelines.

---

## **Key Features**

* **Agentic, Multi-Step Reasoning**

  * Research queries are executed as structured workflows rather than single LLM calls
  * Each reasoning step is explicitly defined and traceable

* **LLM-Powered Summarization**

  * Uses a locally hosted **Mistral-7B** model via **llama.cpp**
  * Generates concise, structured summaries for open-ended research questions

* **Automated Citation Retrieval**

  * Integrates with **Semantic Scholar API**
  * Automatic fallback to **Arxiv API**
  * Extracts titles, abstracts, authors, publication dates, and links

* **Interactive Knowledge Graph**

  * Visualizes relationships between research prompts, summaries, and citations
  * Built using **networkx** and **pyvis**
  * Supports real-time updates as the workflow evolves

* **Node-Based Visual Interface**

  * Powered by **ComfyUI**
  * Allows researchers to initiate, modify, and extend workflows visually

* **Workflow Persistence**

  * Save and reload research sessions using JSON
  * Export graphs in **GraphML** format for external tools like Gephi

---

## **System Architecture**

At a high level, the system consists of:

* **ComfyUI**
  Node-based frontend for user interaction, visualization, and workflow control

* **LangGraph Backend**
  Orchestrates LLM reasoning, citation retrieval, and graph construction as a state machine

* **Local LLM Inference**
  Mistral-7B running via llama.cpp for efficient, local summarization

* **Citation APIs**
  Semantic Scholar and Arxiv for academic metadata retrieval

* **Knowledge Graph Layer**
  networkx and pyvis for graph generation and visualization

*(Detailed architecture diagrams and explanations are available in the project report.)*

---

## **Technology Stack**

* **LangGraph** – Agentic workflow orchestration and state management
* **ComfyUI** – Node-based visual programming interface
* **Mistral-7B** – Large Language Model for summarization and reasoning
* **llama.cpp** – Lightweight local LLM inference
* **Python** – Backend implementation
* **asyncio** – Asynchronous request handling
* **networkx** – Knowledge graph construction
* **pyvis** – Graph visualization
* **Semantic Scholar API** – Academic citation retrieval
* **Arxiv API** – Fallback citation source
* **JSON / GraphML** – Workflow and graph serialization

---

## **How It Works**

1. The user enters a research query through the **ResearchNode** in ComfyUI
2. The query is sent to the backend as structured JSON
3. **LangGraph** orchestrates the workflow:

   * Summarization via Mistral-7B
   * Citation retrieval from academic APIs
   * Knowledge graph construction
4. Results are returned to ComfyUI in real time:

   * Bullet-point summaries
   * Citation popups
   * Interactive graph visualization
5. Users can iterate, refine prompts, and save workflows for later use

---

## **Demo**

📽 **Demo Video:**
Link to be updated

---

## **Future Enhancements**

* PDF and full-text paper ingestion
* In-text citation highlighting
* Multi-agent collaboration
* Multi-user shared research sessions
* Expanded insight clustering and trend analysis



Just tell me what you’d like next.
