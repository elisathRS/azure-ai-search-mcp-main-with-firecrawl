"""
Configuration constants for the hybrid search pipeline.
All tunable parameters live here so they're easy to find and adjust.
"""

import os

# Resolve default docs directory: the project root contains `files_converted/`
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.environ.get(
    "DOCS_DIR",
    os.path.join(_PROJECT_ROOT, "files_converted"),
)

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
CROSS_ENCODER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

BM25_K1 = 1.5       # term-frequency saturation
BM25_B = 0.75        # document-length normalization
RRF_K = 60           # Azure's default constant for Reciprocal Rank Fusion
TOP_K = 50           # results retrieved from each leg
RERANK_TOP_N = 10    # results the semantic reranker evaluates

BANNER = "=" * 80
DIVIDER = "-" * 60
