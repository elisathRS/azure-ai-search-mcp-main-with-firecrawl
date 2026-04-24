"""
Phase 3 (part 1) -- Language Analyzer.

Simulates Azure's language analyzer pipeline:
  tokenization -> lowercasing -> stop-word removal -> stemming

Identical to what the NLTK articles covered, packaged as a reusable analyzer.
"""

import string

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


class TextAnalyzer:

    def __init__(self):
        self.stemmer = PorterStemmer()
        self.stop_words = set(stopwords.words("english"))
        self.punct = set(string.punctuation)

    def analyze(self, text: str) -> list[str]:
        tokens = word_tokenize(text.lower())
        analyzed = []
        for token in tokens:
            token = token.strip(string.punctuation)
            if token and token not in self.stop_words and not all(c in self.punct for c in token):
                analyzed.append(self.stemmer.stem(token))
        return analyzed

    def analyze_verbose(self, text: str) -> dict:
        """Same as analyze() but returns intermediate steps for debugging."""
        raw_tokens = word_tokenize(text.lower())
        after_stopwords = [t for t in raw_tokens if t.strip(string.punctuation) not in self.stop_words]
        after_punct = [t.strip(string.punctuation) for t in after_stopwords]
        after_punct = [t for t in after_punct if t and not all(c in self.punct for c in t)]
        stemmed = [self.stemmer.stem(t) for t in after_punct]
        return {
            "original_tokens": raw_tokens,
            "after_stop_and_punct": after_punct,
            "after_stemming": stemmed,
        }
