# CSI4107 - Assignment 1: Information Retrieval System

## Team Members
- Rina Osman - 300222206
- Fatima Ghadbawi - [student number]
- Name - [student number]

---

## 1. Introduction
(Provide an overview of the project, objectives, and brief summary of the IR system.)

---

## 2. Functionality of the Program
(Describe the functionality of each component in the system: preprocessing, indexing, retrieval, and ranking.)

---

## 3. How to Run the Program
(Step-by-step guide to setting up the environment, running the scripts, and obtaining results.)

### 3.1 Install Dependencies
Ensure you have Python 3.8+ installed. Then, install all required dependencies:

    pip install -r requirements.txt

The required dependencies include:  
- `nltk` (for text preprocessing)  
- `numpy` (for numerical operations)  
- `scipy` (for cosine similarity calculations)  
- `sklearn` (for TF-IDF vectorization)  
- `jsonlines` (for handling `.jsonl` files)  
- `pandas` (for handling tabular data)  

### 3.2 Preprocess the Corpus
Preprocessing extracts, tokenizes, and cleans the text data, then saves it as preprocessed_corpus.jsonl.

    python src/preprocess.py

✅ Expected Output:
data/scifact/preprocessed_corpus.jsonl

### 3.3 Create the Inverted Index
Indexing builds the inverted index, which is necessary for retrieval.

    python src/index.py

✅ Expected Output:
data/scifact/inverted_index.json

### 3.4 Run Document Retrieval and Ranking
Retrieval runs the search system using two different query modes:

Title-only retrieval (results_title.txt)
Title + Full-text retrieval (results_text.txt)

    python src/retrieval.py

✅ Expected Output:
- results/results_title.txt
- results/results_text.txt

The retrieval script: 

    ✔ Loads the preprocessed corpus and inverted index
    ✔ Selects only odd-numbered queries from test.tsv
    ✔ Retrieves relevant documents using TF-IDF + Cosine Similarity
    ✔ Outputs results in TREC format

### 3.5 Evaluate Results using trec_eval
To compute Mean Average Precision (MAP) and other evaluation metrics, run:

    trec_eval data/scifact/qrels/test.tsv results/results_title.txt
    trec_eval data/scifact/qrels/test.tsv results/results_text.txt

This will output evaluation metrics such as:
- Mean Average Precision (MAP)
- Precision at different ranks (P@10, P@20, etc.)
- Recall scores

---

## 4. Algorithms, Data Structures, and Optimizations
- **Preprocessing:** (Explain tokenization, stopword removal, stemming, and any optimizations.)
- **Indexing:** (Describe the inverted index structure and storage.)
- **Retrieval & Ranking:** (Explain cosine similarity or BM25 ranking method.)

---

## 5. Vocabulary Statistics
- **Vocabulary Size:** (Provide the total count of unique tokens.)
- **Sample of 100 Tokens:** (List a random selection of 100 words.)

---

## 6. Query Results & Discussion
- **First 10 Answers for First 2 Queries:** (Present ranked results for sample queries.)
- **Discussion:** (Compare retrieval effectiveness for different query formulations: title-only vs. full-text queries.)

---

## 7. Mean Average Precision (MAP) Score
(Present MAP score computed using `trec_eval` and interpret the results.)

---

## 8. Conclusion
(Summarize key findings, possible improvements, and reflections on system performance.)
