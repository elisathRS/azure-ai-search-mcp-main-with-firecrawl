"""
Phase 4 -- BM25 Scoring.

BM25 (Best Matching 25) -- the modern evolution of TF-IDF.
Improvements over raw TF-IDF:
  - Term-frequency saturation  (100th occurrence != 10x the 10th)
  - Document-length normalization (short docs get a boost)
"""

import math

from config import BM25_K1, BM25_B, TOP_K
from text_analyzer import TextAnalyzer
from inverted_index import InvertedIndex


class BM25Scorer:

    def __init__(self, inv_index: InvertedIndex, k1: float = BM25_K1, b: float = BM25_B):
        self.idx = inv_index
        self.k1 = k1
        self.b = b

    def idf(self, term: str) -> float:
        df = self.idx.document_frequency(term)
        N = self.idx.total_docs
        if df == 0:
            return 0.0
        return math.log((N - df + 0.5) / (df + 0.5) + 1.0)

    def score_document(self, chunk_idx: int, query_terms: list[str], verbose: bool = False) -> tuple[float, dict]:
        score = 0.0
        doc_len = self.idx.doc_lengths.get(chunk_idx, 0)
        avg_dl = self.idx.avg_doc_length
        breakdown = {}

        for term in query_terms:
            tf = self.idx.doc_term_freqs.get(chunk_idx, {}).get(term, 0)
            if tf == 0:
                continue
            idf_val = self.idf(term)
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * (doc_len / avg_dl))
            term_score = idf_val * (numerator / denominator)
            score += term_score
            if verbose:
                breakdown[term] = {
                    "tf": tf,
                    "idf": round(idf_val, 4),
                    "saturation": round(numerator / denominator, 4),
                    "term_score": round(term_score, 4),
                }

        return score, breakdown

    def search(self, query: str, analyzer: TextAnalyzer, top_k: int = TOP_K) -> list[tuple[int, float, dict]]:
        query_terms = analyzer.analyze(query)

        candidates = set()
        for term in query_terms:
            for chunk_idx, _ in self.idx.get_postings(term):
                candidates.add(chunk_idx)

        results = []
        for chunk_idx in candidates:
            score, breakdown = self.score_document(chunk_idx, query_terms, verbose=True)
            if score > 0:
                results.append((chunk_idx, score, breakdown))

        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]
