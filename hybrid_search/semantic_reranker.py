"""
Phase 7 -- Semantic Reranking (L2).

Simulates Azure's semantic ranker -- a deep-learning model adapted from Bing.
Uses a cross-encoder that reads BOTH the query and the document text together,
applying machine reading comprehension to judge true relevance.
"""

from sentence_transformers import CrossEncoder

from config import CROSS_ENCODER_MODEL, RERANK_TOP_N


class SemanticReranker:

    def __init__(self, model_name: str = CROSS_ENCODER_MODEL):
        print(f"    Loading cross-encoder: {model_name}")
        self.model = CrossEncoder(model_name)

    def rerank(
        self, query: str, chunks: list[dict], candidate_indices: list[int], top_n: int = RERANK_TOP_N
    ) -> list[tuple[int, float]]:
        pairs = [(query, chunks[idx]["text"][:512]) for idx in candidate_indices]
        scores = self.model.predict(pairs)

        scored = list(zip(candidate_indices, [float(s) for s in scores]))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_n]
