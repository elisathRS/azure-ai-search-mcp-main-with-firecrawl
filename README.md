# azure-ai-search-mcp

An MCP (Model Context Protocol) server that wraps the
[`azure_ai_search`](../azure_ai_search) hybrid-search script.

On startup the server imports the markdown files from `files_converted/`
exactly the same way the original script does — language analyzer, inverted
index, BM25 scoring, sentence-transformer embeddings, cross-encoder reranker,
all built in-memory. It then exposes two MCP tools:

| Tool | Description |
|------|-------------|
| `search(query)` | Hybrid-search the indexed corpus and return the full pipeline trace |
| `add_url(url)` | Scrape a URL with Firecrawl, save it as Markdown, and rebuild the index |

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

## `add_url` tool

The original server only exposed `search`. A second tool, `add_url`, was added
to let you grow the corpus from inside the chat — no file system access needed.

### What it does

1. **Scrape** — calls Firecrawl (`V1FirecrawlApp.scrape_url`) to download the
   page and convert it to clean Markdown (`only_main_content=True`).
2. **Save** — writes the result as a `.md` file in `files_converted/`, using
   the page's `# H1` heading (or the URL slug as a fallback) as the filename.
3. **Rebuild** — calls `_build_engine()` so the new document is immediately
   searchable through `search`.

```python
@mcp.tool()
def add_url(url: str) -> str:
    app = V1FirecrawlApp(api_key=api_key)
    result = app.scrape_url(url, formats=["markdown"], only_main_content=True)

    # Save the file
    (Path(DOCS_DIR) / filename).write_text(md, encoding="utf-8")

    # Rebuild the index so it becomes searchable immediately
    _engine = _build_engine()
```

### Full workflow from the chat

1. User writes: `"Add this URL: https://..."`
2. Claude Desktop calls the `add_url` tool.
3. `add_url` calls Firecrawl using the key from the config.
4. Firecrawl scrapes the page and returns Markdown content.
5. The `.md` file is saved in `files_converted/`.
6. The index is rebuilt (BM25 + embeddings).
7. The page is now immediately searchable via the `search` tool.

### Requirements

`add_url` requires the `firecrawl-py` package and a **Firecrawl API key**
passed through the server environment (see [Configuration](#configuration)
below).

---

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
with two tools: `search` and `add_url`.

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

### Firecrawl API key (`add_url` only)

`add_url` reads the key from the `FIRECRAWL_API_KEY` environment variable.
The cleanest way to set it is through `claude_desktop_config.json` so Claude
Desktop injects it automatically whenever it launches the server.

#### Locate `claude_desktop_config.json`

**Windows** — press `Win + R`, paste `%APPDATA%\Claude`, and open
`claude_desktop_config.json` with Notepad or VS Code.

**macOS** — open Finder, press `Cmd + Shift + G`, paste
`~/Library/Application Support/Claude`, and open `claude_desktop_config.json`
with TextEdit or your preferred editor.

#### Add the `env` block

```json
{
  "mcpServers": {
    "azure-ai-search": {
      "command": "...",
      "args": ["..."],
      "env": {
        "FIRECRAWL_API_KEY": "fc-your-key-here"
      }
    }
  }
}
```

The server reads it with `os.environ.get("FIRECRAWL_API_KEY")` — the user
never has to type the key manually in the chat.

### Pipeline constants

All pipeline tuning constants live in `hybrid_search/config.py`:

- `EMBEDDING_MODEL` — sentence-transformer for the vector leg
- `CROSS_ENCODER_MODEL` — cross-encoder for semantic reranking
- `BM25_K1`, `BM25_B` — BM25 saturation / length-norm
- `RRF_K`, `TOP_K`, `RERANK_TOP_N` — fusion / retrieval sizes
- `DOCS_DIR` — overridable via the `DOCS_DIR` environment variable

Environment variables read at runtime:

- `FIRECRAWL_API_KEY` — required only by the `add_url` tool; set it in
  `claude_desktop_config.json` (see above)
