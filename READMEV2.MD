# Azure AI Search MCP Server (with Firecrawl & Local Stack)

A professional-grade simulation of the **Azure AI Search Hybrid Search** pipeline, packaged as a Model Context Protocol (MCP) server. 

This project bridges the gap between sophisticated search architectures and local AI workflows. It implements a multi-stage retrieval pipeline (BM25 + Vector + RRF + Reranking) that can run either via cloud-connected agents (Cursor/Claude) or as a **100% private, offline stack** using LM Studio.

## 🏗️ Architecture & Privacy: "No Data Leaves the Machine"

Designed for privacy-conscious environments, this server supports a fully offline runtime topology:

* **Offline Boundary**: All processing happens on your local GPU/CPU.
* **Local Corpus**: Processes your `.md` files mounted directly from your machine.
* **Privacy First**: Once models are cached, you can disable internet access. Your knowledge base and queries never leave your hardware.

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

## 🔧 MCP Tools

This server exposes high-utility tools to your AI agent:

* **`search(query)`**: Executes the full hybrid pipeline and returns a detailed trace + the final answer.
* **`add_url(url)`**: 
    1. Scrapes a webpage using Firecrawl.
    2. Converts it to clean Markdown.
    3. Saves it to your local corpus and rebuilds the engine in real-time.

---

## 🚀 Setup & Installation

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
3.  **Run**: Enable the integration in the chat and start searching your local files.

### Option B: Cloud-Connected (Cursor / Claude Desktop)
1.  **Build**: `docker build -t azure-ai-search-mcp .`
2.  **Environment**: Add your `FIRECRAWL_API_KEY` to your MCP configuration's `env` block to enable the scraping tool.

---

## 📝 UX Optimization: "Final Answer Only"

The `search` tool is verbose by design to provide transparency into the scoring logic. To keep your chat UI clean, we include a **Portable System Rule**:

* **Function**: Instructs the LLM to hide the Step A-E background logs and only render the substantive `FINAL ANSWER` content.
* **Deployment**: Automatically applied via `.cursorrules` or manually added to your **LM Studio System Prompt**.

---

## 🧪 Demo Queries
Try these to see the hybrid engine in action:
* **Keyword Focus**: `AppDXHelper.exe` (Finds exact technical strings).
* **Semantic Focus**: `How do I remove the monitoring software?` (Finds "uninstall" via vector similarity).
* **Hybrid Focus**: `Registry keys for browser extension` (Combines specific terms with conceptual intent).
