# 📘 MCP Local Search Server (Azure AI Search Simulation)

## Overview

This project provides a lightweight **MCP (Model Context Protocol) server** that simulates the behavior of Azure AI Search while running entirely in your own environment.

It enables you to build a powerful, privacy-first retrieval system where your data stays local, yet can be queried and enhanced using advanced language models like Claude or GPT.

At its core, the MCP server exposes a **search tool** that indexes and retrieves knowledge base content (such as internal documentation or markdown files), allowing LLMs to perform contextual reasoning over your data: effectively enabling a **Retrieval-Augmented Generation (RAG)** workflow without relying on external cloud search services.

---

## ⚙️ Key Features

- **Local Search Engine Simulation**  
  Mimics Azure AI Search capabilities for indexing and querying structured/unstructured data.

- **LLM Integration**  
  Works seamlessly with public models like Claude or GPT for enhanced reasoning over your private data.

- **Full Local RAG Support**  
  Includes guidance for integrating with LM Studio, enabling a completely offline pipeline using local models.

- **Web Content Ingestion (`add_url`)**  
  Uses Firecrawl to:
  - Scrape web pages  
  - Convert them into Markdown  
  - Automatically ingest them into your local search index  

- **Markdown-Based Knowledge Base**  
  Simple, portable, and developer-friendly format for storing and querying data.

---

## 🚀 How It Works

1. **Ingest Data**
   - Add local files or scrape web content via `add_url`

2. **Index Content**
   - Content is processed and stored as searchable markdown

3. **Query via MCP**
   - LLMs call the MCP search tool to retrieve relevant context

4. **Generate Responses**
   - Models combine retrieved data with reasoning to produce answers

---

## 💡 Use Cases

### 🔒 Private Knowledge Base Search
Run an internal search system for:
- Support articles  
- Runbooks  
- Internal documentation  

All without exposing sensitive data to external services.

---

### 🤖 AI-Powered Support Assistant
Create a chatbot that:
- Answers customer or internal support questions  
- Uses your real documentation as ground truth  
- Reduces hallucinations by grounding responses in your data  

---

### 🌐 Website Intelligence & Q&A
Use `add_url` to:
- Scrape competitor websites, docs, or public resources  
- Turn them into a searchable dataset  
- Ask questions like:  
  *“What features does this product support?”*

---

### 🧪 Local RAG Development & Testing
Perfect for:
- Prototyping RAG systems without cloud dependencies  
- Testing retrieval strategies locally  
- Experimenting with embeddings and ranking logic  

---

### 🧠 Fully Offline AI Stack
Combine with LM Studio to:
- Run local LLMs  
- Keep all data and inference on your machine  
- Achieve a **zero-cloud AI pipeline**  

---

### 📊 DevOps / Troubleshooting Assistant
Index logs, RCAs, or runbooks and:
- Query issues in natural language  
- Correlate past incidents  
- Speed up debugging workflows  

---

### 📚 Personal Knowledge Management
Turn your notes, PDFs, and saved articles into:
- A searchable second brain  
- An AI assistant that understands your content  

---

## 🎯 Why This Matters

This project bridges the gap between:
- The **power of modern LLMs**
- And the **control of local data ownership**

You get the benefits of AI-driven search and reasoning **without sacrificing privacy, cost control, or flexibility**.

## MCP Tools

This server exposes high-utility tools to your AI agent:

| Tool | Description |
|------|-------------|
| `search(query)` | Hybrid-search the indexed corpus and return the full pipeline trace |
| `add_url(url)` | Scrape a URL with Firecrawl, save it as Markdown, and rebuild the index |

---

## Pipeline

| Phase | Stage                | What it does                                            |
|-------|----------------------|---------------------------------------------------------|
| 1     | Document Ingestion   | Load `.md` files from `files_converted/`                |
| 2     | Chunking             | Split docs into section-level passages                  |
| 3     | Full-Text Indexing   | Tokenize, stem, remove stop words, build inverted index |
| 4     | BM25 Scoring         | Rank by keyword relevance (L1 keyword leg)              |
| 5     | Vector Indexing      | Generate embeddings for each chunk                      |
| 6     | Vector Search        | Cosine similarity nearest neighbors (L1 vector leg)     |
| 7     | Hybrid Merge (RRF)   | Reciprocal Rank Fusion combines both legs               |
| 8     | Semantic Reranking   | Cross-encoder reranks top results (L2)                  |

**Detailed Guides**: For an in-depth explanation of these concepts, visit: [Azure AI Search: NLP at Scale](https://guides.enddesk.com/docs/nlp/azure-ai-search/introduction) and [Hybrid Search: Building the Pipeline from Scratch](https://guides.enddesk.com/docs/nlp/azure-ai-search/hybrid-search)

---

## The Multi-Phase Pipeline

The engine replicates the advanced retrieval logic of Azure AI Search through three distinct phases of development:

| Phase | Component | What it does |
| :--- | :--- | :--- |
| **1** | **Core Search Engine** | Implements **BM25** (Keyword) and **Sentence-Transformers** (Vector) search. |
| **2** | **Hybrid Fusion (RRF)** | Merges keyword and vector results using **Reciprocal Rank Fusion** for balanced relevance. |
| **3** | **Semantic Reranking** | Uses a **Cross-Encoder** to perform deep semantic scoring on top candidates. |
| **+** | **Dynamic Ingestion** | Integrated **Firecrawl** tool to scrape web URLs and rebuild the index instantly. |

---

## Architecture & Privacy: "No Data Leaves the Machine"

Designed for privacy-conscious environments, this server supports a fully offline runtime topology:

* **Offline Boundary**: All processing happens on your local GPU/CPU.
* **Local Corpus**: Processes your `.md` files mounted directly from your machine.
* **Privacy First**: Once models are cached, you can disable internet access. Your knowledge base and queries never leave your hardware.

---

## Setup & Installation

### Option A: Fully Local Stack (LM Studio + Docker)
*Best for total privacy and offline use.*

1.  **Model Selection**: Download a GGUF model with native **Tool Use** capabilities in LM Studio. 
    * **Recommended**: `google/gemma-4-31b` (or any tool-capable model like `gemma-4-4b-it`).
2.  **Config**: In LM Studio, edit your `mcp.json` to include the Docker run command:
    ```json
    {
      "mcpServers": {
        "azure-ai-search": {
          "command": "docker",
          "args": ["run", "--rm", "-i", "azure-ai-search-mcp"]
        }
      }
    }
    ```
3.  **Detailed Guide**: For a step-by-step walkthrough of this local setup, visit: [Local Hybrid Search with LM Studio and MCP](https://guides.enddesk.com/docs/nlp/running-locally/local-hybrid-search).
4.  **Run**: Enable the integration in the chat and start searching your local files.

### Option B: Cloud-Connected (Cursor / Claude Desktop)
1.  **Build**: `docker build -t azure-ai-search-mcp .`
2.  **Environment**: Add your `FIRECRAWL_API_KEY` to your MCP configuration's `env` block to enable the scraping tool.
3.  **Detailed Guide**: For a step-by-step walkthrough of how to configure Firecrawl, visit: [Firecrawl Configuration](https://github.com/elisathRS/azure-ai-search-mcp-main-with-firecrawl/blob/main/firecrawl_configuration.md).

---

## UX Optimization: "Final Answer Only"

The `search` tool is verbose by design to provide transparency into the scoring logic. To keep your chat UI clean, we include a **Portable System Rule**:

* **Function**: Instructs the LLM to hide the Step A-E background logs and only render the substantive `FINAL ANSWER` content.
* **Deployment**: Automatically applied via `.cursorrules` or manually added to your **LM Studio System Prompt**.

---

## Demo Queries

Once the MCP is connected in Cursor/Claude, paste any of these prompts into the chat. Cursor will call the `search` tool with the query and print the full pipeline trace (BM25 breakdown, cosine scores, RRF fusion, cross-encoder reranking, final winner).

* `AppDXHelper.exe`
* `How do I remove the monitoring software from my computer?`
* `How do I enable debug logging for the ControlUp agent?`
* `What steps are needed to set up browser monitoring on Windows?`
* `What registry keys does the browser extension configure?`

### Why these five?
Each one stresses a different leg of the pipeline:
* **AppDXHelper.exe** — Exact keyword match; BM25 shines, while embeddings might dilute it.
* **How do I remove the monitoring software?** — Vocabulary mismatch (docs say "uninstall", not "remove"); the vector leg shines.
* **How do I enable debug logging?** — Specific procedural question; hybrid retrieval picks up both signals.
* **What steps for browser monitoring?** — Broad conceptual question; vector + reranker do the heavy lifting.
* **What registry keys?** — Mixed: keyword (registry) + conceptual intent.

Feel free to ask your own questions too — anything grounded in the markdown files under `files_converted/` should work.

---

## Video Walkthrough

---

## Development Roadmap & Repositories

Follow the evolution of the project through its dedicated phase repositories:

### 🔹 Phase 1: Core Azure AI Search
> **[View Phase 1 Repository ↗](https://github.com/oduenas-enddesk/azure_ai_search)**
> Focuses on structuring the initial indexes, data connections, and backend search logic.

### 🔹 Phase 2: MCP Server Implementation
> **[View Phase 2 Repository ↗](https://github.com/oduenas-enddesk/azure-ai-search-mcp)**
> Contains the implementation for the Model Context Protocol, enabling seamless interaction between the search indexes and AI agents.

### 🔹 Phase 3: Firecrawl Integration (Current)
> **[View Phase 3 Repository ↗](https://github.com/elisathRS/azure-ai-search-mcp-main-with-firecrawl)**
> Introduces dynamic knowledge expansion. This phase allows the system to automatically extract clean web data from a URL, save it as Markdown, and instantly update the search engine without manual file handling


