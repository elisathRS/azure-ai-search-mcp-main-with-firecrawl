# azure-ai-search-mcp

An MCP (Model Context Protocol) server that wraps the
[`azure_ai_search`](../azure_ai_search) hybrid-search script.

On startup the server imports the markdown files from `files_converted/`
exactly the same way the original script does -- language analyzer, inverted
index, BM25 scoring, sentence-transformer embeddings, cross-encoder reranker,
all built in-memory. It then exposes a single MCP tool, `search(query)`, that
returns the full step-by-step pipeline trace for any query you send it.

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

## Project layout

```
azure_ai_search_mcp/
├── hybrid_search/          # the original pipeline, as a package
├── files_converted/        # the markdown corpus the MCP indexes
├── server.py               # MCP server (stdio)
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## Run with Docker (recommended)

The Dockerfile pre-downloads the NLTK corpora and the HuggingFace models at
build time so the MCP boots quickly and works offline afterwards. The server
speaks MCP over **stdio**, so no ports need to be published.

### 1. Build the image

From this directory:

```bash
docker build -t azure-ai-search-mcp .
```

The first build is slow (~2 GB of model weights). Subsequent builds hit the
Docker layer cache.

### 2. Wire it into Cursor as an MCP server

Add this block to your Cursor MCP config (Cursor → Settings → MCP →
"Add new MCP Server", or edit `~/.cursor/mcp.json`):

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

Restart Cursor. You should see `azure-ai-search` listed under MCP Servers
with one tool: `search`.

### 3. Index your own documents (optional)

Mount a directory of markdown files over the baked-in corpus:

```json
{
  "mcpServers": {
    "azure-ai-search": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i",
        "-v", "/absolute/path/to/your/md/files:/app/files_converted:ro",
        "azure-ai-search-mcp"
      ]
    }
  }
}
```

---

## Run locally (without Docker)

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python server.py
```

Then point Cursor at it:

```json
{
  "mcpServers": {
    "azure-ai-search": {
      "command": "/absolute/path/to/.venv/bin/python",
      "args": ["/absolute/path/to/azure_ai_search_mcp/server.py"]
    }
  }
}
```

---

## Demo queries

Once the MCP is connected in Cursor, paste any of these prompts into the chat.
Cursor will call the `search` tool with the query and print the full
pipeline trace (BM25 breakdown, cosine scores, RRF fusion, cross-encoder
reranking, final winner).

> `AppDXHelper.exe`

> `How do I remove the monitoring software from my computer?`

> `How do I enable debug logging for the ControlUp agent?`

> `What steps are needed to set up browser monitoring on Windows?`

> `What registry keys does the browser extension configure?`

### Why these five?

Each one stresses a different leg of the pipeline -- same rationale as the
original script:

1. **`AppDXHelper.exe`** — exact keyword match; BM25 shines, embeddings dilute it.
2. **`How do I remove the monitoring software from my computer?`** — vocabulary
   mismatch (docs say "uninstall", not "remove"); vector leg shines.
3. **`How do I enable debug logging for the ControlUp agent?`** — specific
   procedural question; hybrid picks up both signals.
4. **`What steps are needed to set up browser monitoring on Windows?`** — broad
   conceptual question; vector + reranker do the heavy lifting.
5. **`What registry keys does the browser extension configure?`** — mixed:
   keyword (`registry`) + conceptual intent.

Feel free to ask your own questions too — anything grounded in the markdown
files under `files_converted/` should work.

---

## Cursor rule: return only the final answer

By default the `search` tool returns the **full pipeline trace** (Step A
language analysis, Step B BM25, Step C vector search, Step D RRF fusion,
Step E semantic reranking, and the `FINAL ANSWER` block). That is great for
demos, but often you just want the answer.

This repo ships a Cursor rule that handles that client-side:

```
.cursor/rules/azure-ai-search-final-answer-only.mdc
```

The rule has `alwaysApply: true` and instructs the agent to surface **only
the `FINAL ANSWER` chunk** to the user when it calls
`user-azure-ai-search.search`, unless the user explicitly asks for the
pipeline trace / scores / reranking details.

### How to use it

1. Open this project in Cursor (the rule is auto-loaded from
   `.cursor/rules/`).
2. Ask any question that should be answered from the indexed corpus — e.g.
   *"How do I remove the monitoring software from my computer?"*
3. The agent will call `search`, then reply with just the final answer
   chunk. If you want the full trace, ask for it explicitly ("show me the
   full pipeline trace" / "show the BM25 and vector scores").

---

## Configuration

All pipeline constants live in `hybrid_search/config.py`:

- `EMBEDDING_MODEL` — sentence-transformer for the vector leg
- `CROSS_ENCODER_MODEL` — cross-encoder for semantic reranking
- `BM25_K1`, `BM25_B` — BM25 saturation / length-norm
- `RRF_K`, `TOP_K`, `RERANK_TOP_N` — fusion / retrieval sizes
- `DOCS_DIR` — overridable via the `DOCS_DIR` environment variable
