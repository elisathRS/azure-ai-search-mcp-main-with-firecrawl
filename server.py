"""
MCP server wrapping the azure_ai_search hybrid search pipeline.

On startup it loads the markdown corpus from `files_converted/` and builds the
full hybrid index (BM25 + embeddings + cross-encoder), exactly like running the
original script. It then exposes one MCP tool -- `search(query)` -- that returns
the step-by-step pipeline output for any query you send it.
"""

from __future__ import annotations

import contextlib
import io
import os
import re
import sys
from pathlib import Path

import nltk
from mcp.server.fastmcp import FastMCP

# Make the hybrid_search package importable and then build the engine.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from hybrid_search.config import DOCS_DIR  # noqa: E402
from hybrid_search.hybrid_engine import HybridSearchEngine  # noqa: E402


def _log(msg: str) -> None:
    # MCP stdio uses stdout for JSON-RPC; all human logs must go to stderr.
    print(msg, file=sys.stderr, flush=True)


def _ensure_nltk_data() -> None:
    for pkg in ("punkt", "punkt_tab", "stopwords"):
        nltk.download(pkg, quiet=True)


def _build_engine() -> HybridSearchEngine:
    _log(f"[azure-ai-search-mcp] Building index from {DOCS_DIR} ...")
    engine = HybridSearchEngine()
    # The engine prints verbosely to stdout during indexing. Redirect to stderr
    # so we do not corrupt the MCP stdio channel.
    with contextlib.redirect_stdout(sys.stderr):
        engine.build_index(DOCS_DIR)
    _log("[azure-ai-search-mcp] Index ready. Waiting for queries...")
    return engine


_ensure_nltk_data()
_engine = _build_engine()

mcp = FastMCP("azure-ai-search")


@mcp.tool()
def search(query: str) -> str:
    """
    Run a hybrid-search query against the indexed markdown corpus.

    Returns the full step-by-step pipeline trace (language analysis, BM25,
    vector search, RRF fusion, semantic reranking, and the final best chunk).

    Args:
        query: Natural-language query or exact keyword to search for.
    """
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        _engine.search(query)
    return buf.getvalue()


def _slugify(text: str) -> str:
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text.strip())
    return text[:80]


def _title_from_markdown(md: str, fallback: str) -> str:
    for line in md.splitlines():
        if line.strip().startswith("# "):
            return line.strip()[2:].strip()
    return fallback


@mcp.tool()
def add_url(url: str) -> str:
    """
    Scrape a URL with Firecrawl, save it as a markdown file in files_converted/,
    and rebuild the search index so it is immediately searchable.

    Requires FIRECRAWL_API_KEY to be set in the server environment.

    Args:
        url: Full URL to scrape (e.g. https://support.controlup.com/docs/...).
    """
    api_key = os.environ.get("FIRECRAWL_API_KEY")
    if not api_key:
        return "Error: FIRECRAWL_API_KEY is not configured in Claude Desktop settings."

    try:
        from firecrawl import V1FirecrawlApp
        app = V1FirecrawlApp(api_key=api_key)
        result = app.scrape_url(url, formats=["markdown"], only_main_content=True)
        md = result.markdown or ""
        if not md.strip():
            return f"Error: no content returned for {url} — the page may require a login."

        url_slug = _slugify(url.rstrip("/").split("/")[-1])
        title = _title_from_markdown(md, url_slug)
        filename = _slugify(title) + ".md"

        Path(DOCS_DIR).mkdir(exist_ok=True)
        (Path(DOCS_DIR) / filename).write_text(md, encoding="utf-8")

        global _engine
        _engine = _build_engine()

        words = len(md.split())
        return f"✓ Saved '{filename}' ({words} words). Index rebuilt — you can search it now."

    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    mcp.run()
