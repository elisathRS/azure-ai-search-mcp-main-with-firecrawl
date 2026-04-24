"""
Utility functions -- standalone helpers that don't belong to a specific class.

Covers:
  - Document ingestion  (load_documents)
  - Chunking            (chunk_document, chunk_all_documents)
  - Rank fusion         (reciprocal_rank_fusion)
"""

import os
import re
from collections import defaultdict

from config import RRF_K


# -- Document ingestion ------------------------------------------------

def load_documents(docs_dir: str) -> list[dict]:
    """Load every .md file from the directory -- same as importing docs into Azure AI Search."""
    documents = []
    for filename in sorted(os.listdir(docs_dir)):
        if filename.endswith(".md"):
            filepath = os.path.join(docs_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            documents.append({
                "id": filename,
                "filename": filename,
                "content": content,
            })
    return documents


# -- Chunking ----------------------------------------------------------

def chunk_document(doc: dict) -> list[dict]:
    """
    Split one document into chunks by markdown headings (## or ###).
    Azure AI Search does the same -- large documents get broken into
    one-to-two-paragraph passages before indexing.
    """
    content = doc["content"]
    sections = re.split(r"\n(?=#{1,3}\s)", content)

    chunks = []
    for i, section in enumerate(sections):
        text = section.strip()
        if not text or len(text) < 30:
            continue
        heading_match = re.match(r"^(#{1,3})\s+(.+)", text)
        heading = heading_match.group(2) if heading_match else "Intro / preamble"

        chunks.append({
            "chunk_id": f"{doc['id']}::chunk_{i}",
            "doc_id": doc["id"],
            "doc_filename": doc["filename"],
            "heading": heading,
            "text": text,
        })
    return chunks


def chunk_all_documents(documents: list[dict]) -> list[dict]:
    all_chunks = []
    for doc in documents:
        all_chunks.extend(chunk_document(doc))
    return all_chunks


# -- Reciprocal Rank Fusion -------------------------------------------

def reciprocal_rank_fusion(
    keyword_results: list[tuple[int, float, dict]],
    vector_results: list[tuple[int, float]],
    k: int = RRF_K,
) -> list[tuple[int, float, dict]]:
    """
    RRF merges two ranked lists without needing scores on the same scale.
    Formula: RRF(doc) = SUM( 1/(k + rank_i) )  for each ranker i
    """
    rrf_scores: dict[int, float] = defaultdict(float)
    debug: dict[int, dict] = defaultdict(lambda: {
        "kw_rank": None, "kw_score": None, "kw_breakdown": None,
        "vec_rank": None, "vec_score": None,
        "kw_rrf_contrib": 0.0, "vec_rrf_contrib": 0.0,
    })

    for rank, (idx, score, breakdown) in enumerate(keyword_results, start=1):
        contrib = 1.0 / (k + rank)
        rrf_scores[idx] += contrib
        debug[idx]["kw_rank"] = rank
        debug[idx]["kw_score"] = score
        debug[idx]["kw_breakdown"] = breakdown
        debug[idx]["kw_rrf_contrib"] = contrib

    for rank, (idx, score) in enumerate(vector_results, start=1):
        contrib = 1.0 / (k + rank)
        rrf_scores[idx] += contrib
        debug[idx]["vec_rank"] = rank
        debug[idx]["vec_score"] = score
        debug[idx]["vec_rrf_contrib"] = contrib

    merged = [(idx, rrf_score, debug[idx]) for idx, rrf_score in rrf_scores.items()]
    merged.sort(key=lambda x: x[1], reverse=True)
    return merged
