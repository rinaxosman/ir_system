import json
from collections import defaultdict
from preprocess import Preprocessor

class Retriever:
    def __init__(self, index_file="../data/scifact/inverted_index.json"):
        with open(index_file, "r") as f:
            data = json.load(f)
            self.inverted_index = data["index"]
            self.doc_lengths = data["doc_lengths"]
        self.preprocessor = Preprocessor()

    def compute_similarity(self, query_tokens):
        scores = defaultdict(float)
        for term in query_tokens:
            if term in self.inverted_index:
                for doc_id, tf in self.inverted_index[term].items():
                    scores[doc_id] += tf  

        for doc_id in scores:
            scores[doc_id] /= self.doc_lengths.get(doc_id, 1)
        
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)

    def search(self, query, top_k=10):
        query_tokens = self.preprocessor.preprocess_text(query)
        return self.compute_similarity(query_tokens)[:top_k]

if __name__ == "__main__":
    retriever = Retriever()
    print(retriever.search("What are the effects of COVID-19?"))