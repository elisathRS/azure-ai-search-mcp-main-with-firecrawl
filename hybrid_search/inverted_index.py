"""
Phase 3 (part 2) -- Inverted Index.

The same data structure behind every search engine.
Maps each stemmed term to the list of chunks that contain it:

    "uninstal"       -> [chunk_0 (tf=2), chunk_3 (tf=1)]
    "appdxhelper.ex" -> [chunk_0 (tf=3), chunk_5 (tf=1)]
"""

from collections import defaultdict, Counter

from text_analyzer import TextAnalyzer


class InvertedIndex:

    def __init__(self, analyzer: TextAnalyzer):
        self.analyzer = analyzer
        self.index: dict[str, list[tuple[int, int]]] = defaultdict(list)
        self.doc_lengths: dict[int, int] = {}
        self.doc_term_freqs: dict[int, Counter] = {}
        self.total_docs = 0
        self.avg_doc_length = 0.0

    def build(self, chunks: list[dict]):
        self.total_docs = len(chunks)
        total_length = 0

        for idx, chunk in enumerate(chunks):
            tokens = self.analyzer.analyze(chunk["text"])
            self.doc_lengths[idx] = len(tokens)
            total_length += len(tokens)

            tf = Counter(tokens)
            self.doc_term_freqs[idx] = tf

            for term, freq in tf.items():
                self.index[term].append((idx, freq))

        self.avg_doc_length = total_length / self.total_docs if self.total_docs else 0

    def get_postings(self, term: str) -> list[tuple[int, int]]:
        return self.index.get(term, [])

    def document_frequency(self, term: str) -> int:
        return len(self.index.get(term, []))
