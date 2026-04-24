"""
Phase 5 -- Vector Index (Embeddings).

Stores dense embeddings for every chunk.
At query time, finds nearest neighbors via exhaustive KNN
(cosine similarity against every vector -- like Azure's eKNN option).
"""

import numpy as np
from sentence_transformers import SentenceTransformer

from config import EMBEDDING_MODEL, TOP_K


class VectorIndex:

    def __init__(self, model_name: str = EMBEDDING_MODEL):
        print(f"    Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.embeddings: np.ndarray | None = None

    def build(self, chunks: list[dict]):
        texts = [chunk["text"] for chunk in chunks]
        print(f"    Encoding {len(texts)} chunks...")
        self.embeddings = self.model.encode(texts, show_progress_bar=True, convert_to_numpy=True)

    def search(self, query: str, top_k: int = TOP_K) -> list[tuple[int, float]]:
        query_emb = self.model.encode([query], convert_to_numpy=True)

        q_norm = query_emb / np.linalg.norm(query_emb, axis=1, keepdims=True)
        d_norms = self.embeddings / np.linalg.norm(self.embeddings, axis=1, keepdims=True)

        similarities = np.dot(d_norms, q_norm.T).flatten()
        top_indices = np.argsort(similarities)[::-1][:top_k]

        return [(int(i), float(similarities[i])) for i in top_indices]
