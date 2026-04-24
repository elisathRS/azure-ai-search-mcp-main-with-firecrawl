"""
hybrid_search -- Simulates the complete Azure AI Search Hybrid Search pipeline.

Pipeline:
  Phase 1: Document Ingestion   - Load .md files
  Phase 2: Chunking             - Split docs into section-level passages
  Phase 3: Full-Text Indexing   - Tokenize, stem, remove stop words, build inverted index
  Phase 4: BM25 Scoring         - Rank by keyword relevance (L1 keyword leg)
  Phase 5: Vector Indexing      - Generate embeddings for each chunk
  Phase 6: Vector Search        - Cosine similarity nearest neighbors (L1 vector leg)
  Phase 7: Hybrid Merge (RRF)   - Reciprocal Rank Fusion combines both legs
  Phase 8: Semantic Reranking   - Cross-encoder reranks top results (L2)
"""

import sys
from pathlib import Path

_pkg_dir = str(Path(__file__).resolve().parent)
if _pkg_dir not in sys.path:
    sys.path.insert(0, _pkg_dir)

from text_analyzer import TextAnalyzer
from inverted_index import InvertedIndex
from bm25_scorer import BM25Scorer
from vector_index import VectorIndex
from semantic_reranker import SemanticReranker
from hybrid_engine import HybridSearchEngine
from utils import load_documents, chunk_document, chunk_all_documents, reciprocal_rank_fusion

__all__ = [
    "TextAnalyzer",
    "InvertedIndex",
    "BM25Scorer",
    "VectorIndex",
    "SemanticReranker",
    "HybridSearchEngine",
    "load_documents",
    "chunk_document",
    "chunk_all_documents",
    "reciprocal_rank_fusion",
]
