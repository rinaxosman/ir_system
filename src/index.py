import json
import math
import os
from collections import defaultdict
from preprocess import Preprocessor

class Indexer:
    def __init__(self):
        self.inverted_index = defaultdict(dict)
        self.doc_lengths = {}

    def build_index(self, corpus):
        doc_count = len(corpus)
        for doc_id, tokens in corpus:
            term_freqs = defaultdict(int)
            for token in tokens:
                term_freqs[token] += 1
            
            for term, tf in term_freqs.items():
                self.inverted_index[term][doc_id] = tf
            
            self.doc_lengths[doc_id] = math.sqrt(sum(tf**2 for tf in term_freqs.values()))

        return self.inverted_index

    def save_index(self, filename="../data/scifact/inverted_index.json"):
        # Ensure the directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        # Save the index
        with open(filename, "w") as f:
            json.dump({"index": self.inverted_index, "doc_lengths": self.doc_lengths}, f)

if __name__ == "__main__":
    preprocessor = Preprocessor()
    corpus = preprocessor.preprocess_corpus()
    
    indexer = Indexer()
    index = indexer.build_index(corpus)
    indexer.save_index()