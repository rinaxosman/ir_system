import os
import json
from preprocess import Preprocessor
from index import Indexer
from retrieval import Retriever

def main():
    # Get the base directory of main.py
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct absolute paths for required files
    corpus_path = os.path.join(base_dir, "..", "data", "scifact", "corpus.jsonl")
    queries_path = os.path.join(base_dir, "..", "data", "scifact", "queries.jsonl")
    results_path = os.path.join(base_dir, "..", "results", "Results.txt")

    # Step 1: Preprocessing
    print("[INFO] Starting Preprocessing...")
    preprocessor = Preprocessor()
    
    if not os.path.exists(corpus_path):
        raise FileNotFoundError(f"[ERROR] Corpus file not found: {corpus_path}")

    corpus = preprocessor.preprocess_corpus(corpus_path)
    print(f"[INFO] Processed {len(corpus)} documents.")

    # Step 2: Indexing
    print("[INFO] Building Index...")
    indexer = Indexer()
    indexer.build_index(corpus)
    indexer.save_index()
    print("[INFO] Indexing completed and saved.")

    # Step 3: Retrieval
    print("[INFO] Starting Retrieval...")
    retriever = Retriever()

    # Ensure queries file exists
    if not os.path.exists(queries_path):
        raise FileNotFoundError(f"[ERROR] Queries file not found: {queries_path}")

    # Load queries.jsonl properly
    with open(queries_path, "r", encoding="utf-8") as f:
        queries = [json.loads(line) for line in f]  # Read line-by-line (JSONL format)

    print(f"[INFO] Loaded {len(queries)} queries.")

    # Ensure results directory exists
    os.makedirs(os.path.dirname(results_path), exist_ok=True)

    with open(results_path, "w", encoding="utf-8") as f:
        for query in queries:
            query_id = query["_id"]
            query_text = query["text"]
            top_docs = retriever.search(query_text, top_k=100)

            # Debugging: Print query & retrieved documents
            print(f"[DEBUG] Query ID: {query_id}, Query: {query_text}")
            print(f"[DEBUG] Retrieved {len(top_docs)} documents.")

            if not top_docs:
                print(f"[WARNING] No results found for query ID {query_id}")

            for rank, (doc_id, score) in enumerate(top_docs, 1):
                f.write(f"{query_id} Q0 {doc_id} {rank} {score:.4f} run1\n")


    print(f"[INFO] Retrieval completed. Results saved to: {results_path}")

if __name__ == "__main__":
    main()
