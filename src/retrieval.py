import json
import numpy as np
import re
import pandas as pd
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk

nltk.download("stopwords")
stop_words = set(stopwords.words("english"))
stemmer = PorterStemmer()

def preprocess_text(text):
    """Preprocess text (lowercase, remove special characters, tokenize, remove stopwords, stem)."""
    text = text.lower()
    text = re.sub(r'\W+', ' ', text)
    tokens = text.split()
    tokens = [stemmer.stem(word) for word in tokens if word not in stop_words]
    return " ".join(tokens)

test_queries_path = "data/scifact/qrels/test.tsv"
preprocessed_corpus_path = "data/scifact/preprocessed_corpus.json"

# preprocessed corpus
with open(preprocessed_corpus_path, 'r', encoding='utf-8') as f:
    preprocessed_corpus = json.load(f)

corpus_dict = {str(doc["doc_id"]): " ".join(doc["tokens"]) for doc in preprocessed_corpus}
df = pd.read_csv(test_queries_path, sep="\t", names=["query_id", "corpus_id", "score"])
df["query_id"] = pd.to_numeric(df["query_id"], errors='coerce')

# Filter for only odd-numbered queries
odd_queries = df[df["query_id"] % 2 == 1]

unique_odd_queries = odd_queries.groupby("query_id")["corpus_id"].first().reset_index()

# Extracts thequeries using the corpus_id
test_queries = {}
for _, row in unique_odd_queries.iterrows():
    query_id = int(row["query_id"])
    corpus_id = str(row["corpus_id"]) 
    if corpus_id in corpus_dict:  
        test_queries[query_id] = {
            "query": corpus_dict[corpus_id],
            "run_name": f"run_{corpus_id}_exact"
        }

# Initialize TF-IDF Vectorizer
doc_texts = list(corpus_dict.values())
vectorizer = TfidfVectorizer()
doc_vectors = vectorizer.fit_transform(doc_texts)  # Transform corpus into TF-IDF vectors

def retrieve_and_rank(query, query_id, run_name, top_k=100):
    """Retrieve and rank documents based on cosine similarity."""
    query = preprocess_text(query)  # Preprocess query
    query_vector = vectorizer.transform([query])  # Convert to TF-IDF vector
    similarities = cosine_similarity(query_vector, doc_vectors)[0]  # Compute cosine similarity

    # Rank documents by similarity score
    ranked_docs = sorted(zip(corpus_dict.keys(), similarities), key=lambda x: x[1], reverse=True)[:top_k]

    # Format results
    results = []
    for rank, (doc_id, score) in enumerate(ranked_docs, start=1):
        results.append(f"{query_id} Q0 {doc_id} {rank} {score:.4f} {run_name}")
    
    return results

# Run retrieval for all queries
all_results = []
for query_id, data in test_queries.items():
    all_results.extend(retrieve_and_rank(data["query"], query_id, data["run_name"]))

results_path = "results/Results.txt"
with open(results_path, "w", encoding="utf-8") as f:
    f.write("\n".join(all_results) + "\n")

print(f"✅ Results saved to {results_path}")
