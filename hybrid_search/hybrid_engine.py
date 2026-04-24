"""
The complete Hybrid Search Engine -- orchestrates the full pipeline.

  index -> keyword search (BM25) -> vector search (cosine) -> RRF merge -> semantic rerank
"""

from config import BANNER, DIVIDER, RRF_K, RERANK_TOP_N
from text_analyzer import TextAnalyzer
from inverted_index import InvertedIndex
from bm25_scorer import BM25Scorer
from vector_index import VectorIndex
from semantic_reranker import SemanticReranker
from utils import load_documents, chunk_all_documents, reciprocal_rank_fusion


class HybridSearchEngine:

    def __init__(self):
        self.chunks: list[dict] = []
        self.analyzer = TextAnalyzer()
        self.inverted_index = InvertedIndex(self.analyzer)
        self.bm25: BM25Scorer | None = None
        self.vector_index: VectorIndex | None = None
        self.reranker: SemanticReranker | None = None

    # -- Indexing ---------------------------------------------------

    def build_index(self, docs_dir: str):
        print(f"\n{BANNER}")
        print("  PHASE 1 -- DOCUMENT INGESTION")
        print(BANNER)
        documents = load_documents(docs_dir)
        for doc in documents:
            print(f"    + Loaded: {doc['filename']}  ({len(doc['content']):,} chars)")
        print(f"\n    Total documents: {len(documents)}")

        print(f"\n{BANNER}")
        print("  PHASE 2 -- CHUNKING (splitting docs into passages)")
        print(BANNER)
        self.chunks = chunk_all_documents(documents)
        for i, chunk in enumerate(self.chunks):
            preview = chunk["text"][:90].replace("\n", " ")
            print(f"    chunk[{i}]  {chunk['doc_filename']}  ->  \"{chunk['heading']}\"")
            print(f"             {preview}...")
        print(f"\n    Total chunks: {len(self.chunks)}")

        print(f"\n{BANNER}")
        print("  PHASE 3 -- FULL-TEXT INDEXING (Inverted Index)")
        print(BANNER)
        self.inverted_index.build(self.chunks)
        self.bm25 = BM25Scorer(self.inverted_index)
        print(f"    Unique terms indexed: {len(self.inverted_index.index):,}")
        print(f"    Average chunk length: {self.inverted_index.avg_doc_length:.1f} tokens")

        print(f"\n    +-- Sample inverted-index entries --------------------------")
        sample_terms = sorted(self.inverted_index.index.keys())[:15]
        for term in sample_terms:
            postings = self.inverted_index.get_postings(term)
            entries = ", ".join(f"chunk[{idx}](tf={tf})" for idx, tf in postings)
            print(f"    |  \"{term}\" -> [{entries}]")
        print(f"    +--------------------------------------------------------------")

        print(f"\n{BANNER}")
        print("  PHASE 4 -- VECTOR INDEXING (Generating Embeddings)")
        print(BANNER)
        self.vector_index = VectorIndex()
        self.vector_index.build(self.chunks)
        rows, dims = self.vector_index.embeddings.shape
        print(f"    Embeddings matrix: {rows} chunks x {dims} dimensions")
        print(f"    (same math as SentenceTransformer.encode() from the NLP articles)")

        print(f"\n{BANNER}")
        print("  LOADING SEMANTIC RERANKER (L2 cross-encoder)")
        print(BANNER)
        self.reranker = SemanticReranker()
        print(f"    Ready.\n")

    # -- Query ------------------------------------------------------

    def search(self, query: str):
        print(f"\n{'#' * 80}")
        print(f"#  QUERY: \"{query}\"")
        print(f"{'#' * 80}")

        # -- A. Analyze query --------------------------------------
        steps = self.analyzer.analyze_verbose(query)
        query_terms = steps["after_stemming"]
        print(f"\n{DIVIDER}")
        print(f"  STEP A -- Language Analyzer (query processing)")
        print(DIVIDER)
        print(f"    Original query:    \"{query}\"")
        print(f"    Tokens:            {steps['original_tokens']}")
        print(f"    After stop/punct:  {steps['after_stop_and_punct']}")
        print(f"    After stemming:    {steps['after_stemming']}")

        # -- B. Full-Text Search (BM25) ----------------------------
        kw_results = self.bm25.search(query, self.analyzer)
        print(f"\n{DIVIDER}")
        print(f"  STEP B -- Full-Text Search (BM25 scoring)")
        print(DIVIDER)
        print(f"    Searched inverted index for terms: {query_terms}")
        if kw_results:
            for rank, (idx, score, breakdown) in enumerate(kw_results, 1):
                c = self.chunks[idx]
                print(f"\n    Rank {rank}:  chunk[{idx}]  BM25 = {score:.4f}")
                print(f"      Source: {c['doc_filename']}  /  {c['heading']}")
                for term, info in breakdown.items():
                    print(f"      term \"{term}\": tf={info['tf']}, idf={info['idf']}, "
                          f"saturation={info['saturation']}, contribution={info['term_score']}")
        else:
            print(f"    (no keyword matches found)")

        # -- C. Vector Search (Cosine Similarity) ------------------
        vec_results = self.vector_index.search(query)
        print(f"\n{DIVIDER}")
        print(f"  STEP C -- Vector Search (cosine similarity)")
        print(DIVIDER)
        print(f"    Query embedded to {self.vector_index.embeddings.shape[1]}-dim vector, "
              f"compared against all {len(self.chunks)} chunks")
        for rank, (idx, score) in enumerate(vec_results[:10], 1):
            c = self.chunks[idx]
            print(f"    Rank {rank}:  chunk[{idx}]  cosine = {score:.4f}  "
                  f"<- {c['doc_filename']}  /  {c['heading']}")

        # -- D. Reciprocal Rank Fusion -----------------------------
        rrf_results = reciprocal_rank_fusion(kw_results, vec_results)
        print(f"\n{DIVIDER}")
        print(f"  STEP D -- Reciprocal Rank Fusion (merging both legs)")
        print(DIVIDER)
        print(f"    Formula:  RRF(doc) = SUM( 1/(k + rank_i) )   where k = {RRF_K}")
        print()
        for rank, (idx, rrf_score, info) in enumerate(rrf_results[:10], 1):
            c = self.chunks[idx]
            kw_str = (f"kw_rank={info['kw_rank']}, 1/({RRF_K}+{info['kw_rank']})="
                      f"{info['kw_rrf_contrib']:.6f}" if info["kw_rank"] else "-- (not in keyword results)")
            vec_str = (f"vec_rank={info['vec_rank']}, 1/({RRF_K}+{info['vec_rank']})="
                       f"{info['vec_rrf_contrib']:.6f}" if info["vec_rank"] else "-- (not in vector results)")

            in_both = info["kw_rank"] is not None and info["vec_rank"] is not None
            boost_tag = "  ** IN BOTH LEGS **" if in_both else ""

            print(f"    Rank {rank}:  chunk[{idx}]  RRF = {rrf_score:.6f}{boost_tag}")
            print(f"      Source:  {c['doc_filename']}  /  {c['heading']}")
            print(f"      Keyword: {kw_str}")
            print(f"      Vector:  {vec_str}")

        # -- E. Semantic Reranking (L2) ----------------------------
        top_indices = [idx for idx, _, _ in rrf_results[:RERANK_TOP_N]]
        reranked = self.reranker.rerank(query, self.chunks, top_indices)
        print(f"\n{DIVIDER}")
        print(f"  STEP E -- Semantic Reranking (L2 cross-encoder)")
        print(DIVIDER)
        print(f"    Cross-encoder reads the query + each chunk's text together")
        print(f"    and judges true relevance via reading comprehension.")
        print(f"    Reranking top {len(top_indices)} RRF results...\n")
        for rank, (idx, score) in enumerate(reranked, 1):
            c = self.chunks[idx]
            preview = c["text"][:150].replace("\n", " ")
            print(f"    Rank {rank}:  chunk[{idx}]  rerank_score = {score:.4f}")
            print(f"      Source:  {c['doc_filename']}  /  {c['heading']}")
            print(f"      Preview: {preview}...")

        # -- Final Answer ------------------------------------------
        winner_idx, winner_score = reranked[0]
        winner = self.chunks[winner_idx]
        print(f"\n{BANNER}")
        print(f"  FINAL ANSWER")
        print(BANNER)
        print(f"    Best match:  {winner['doc_filename']}  /  {winner['heading']}")
        print(f"    Score:       {winner_score:.4f}")
        print(f"\n    +-- Chunk text ------------------------------------------------")
        for line in winner["text"].split("\n")[:12]:
            print(f"    |  {line}")
        print(f"    |  ...")
        print(f"    +--------------------------------------------------------------")

        return reranked
