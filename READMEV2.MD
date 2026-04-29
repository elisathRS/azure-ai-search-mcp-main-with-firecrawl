# Azure AI Search MCP Server (with Firecrawl & Local Stack)

A professional-grade simulation of the **Azure AI Search Hybrid Search** pipeline, packaged as a Model Context Protocol (MCP) server. 

This project bridges the gap between sophisticated search architectures and local AI workflows. It implements a multi-stage retrieval pipeline (BM25 + Vector + RRF + Reranking) that can run either via cloud-connected agents (Cursor/Claude) or as a **100% private, offline stack** using LM Studio.

## MCP Tools

This server exposes high-utility tools to your AI agent:

| Tool | Description |
|------|-------------|
| `search(query)` | Hybrid-search the indexed corpus and return the full pipeline trace |
| `add_url(url)` | Scrape a URL with Firecrawl, save it as Markdown, and rebuild the index |

---

## Pipeline (unchanged from the original script)

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

---

## 🛠️ The Multi-Phase Pipeline

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
