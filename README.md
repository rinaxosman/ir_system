# CSI4107 - Assignment 1: Information Retrieval System

## Team Members
- Rina Osman - 300222206
- Fatima Ghadbawi - 300301842
- Uvil Dahanayake - 300199138

## Contributions

Fatima Ghadbawi
- Step 1 (Preprocessing): Developed the text preprocessing pipeline, including tokenization, stopword removal, stemming, and text cleaning.
- Processed the SciFact dataset and structured it into preprocessed_corpus.jsonl for indexing.
- Extracted the total vocabulary size and generated a sample of 100 tokens for reporting.
- Explained the algorithms, data structures, and optimizations used in preprocessing, indexing, and retrieval.
- Report Sections: #4, #5

Rina Osman
- Step 2 (Indexing): Built the inverted index and structured it for efficient document retrieval.
- Step 3 (Retrieval & Ranking): Implemented cosine similarity to rank documents based on relevance to queries.
- Processed and formatted the system output into Results.txt in TREC format.
- Compared retrieval effectiveness between title-only and full-text queries.
- Report Sections: #3, #6, #8


Uvil Dahanayake
- Ran trec_eval to compute Mean Average Precision (MAP) and analyzed evaluation metrics.
- Assisted in comparing retrieval performance for different query modes.
- Contributed to writing and structuring key report sections.
- Wrote sections for Introduction, Functionality of the Program, Query Results & Discussion, and Mean Average Precision (MAP) Score.
- Report Sections: #1, #2, #7

---

## 1. Introduction

- This project aims to build a simple information retrieval system that can search a given collection of documents, in our case a collection provided by Scifact, and return a list of related documents each with its own ranking and score.

---

## 2. Functionality of the Program

- The first stage is preprocessing in which our program goes through each document removing and formatting text in a way that makes it easier to search through and create a more meaningful index. We removed punctuation, numbers, and stopwords while also using the Porter stemmer to normalize similar words that have different inflexional endings before finally saving the processed corpus. 
- We then move on to indexing where we go through each of the preprocessed documents and add tokens to our inverted index with the document ID in which they appear. 
- With our inverted index made we can now retrieve related documents and assign them a score based on cosine similarity.

---

## 3. How to Run the Program

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

- ✔ Loads the preprocessed corpus and inverted index
- ✔ Selects only odd-numbered queries from test.tsv
- ✔ Retrieves relevant documents using TF-IDF + Cosine Similarity
- ✔ Outputs results in TREC format

### 3.5 Evaluate Results using trec_eval
To compute Mean Average Precision (MAP) and other evaluation metrics, run:

    trec_eval data/scifact/qrels/test.tsv results/results_title.txt
    trec_eval data/scifact/qrels/test.tsv results/results_text.txt

This will output evaluation metrics such as:
- Mean Average Precision (MAP)
- Precision at different ranks
- Recall scores

---

## 4. Algorithms, Data Structures, and Optimizations
- **Preprocessing:** Through preprocessing, we tokenize each document before attempting any information retrieval. Tokenization is effectively splitting up the text within each document into an array of terms, this way when checking querying documents we can check to see if they have our queried terms rather than using some sliding window method. Of course, documents will have a lot of words that are duplicates or conjugations of one or even strings that aren't words such as punctuation. This is where we use stopword removal to remove punctuation and special characters and use stemming to group together what is in essence the same word just with different endings due to tense or plurality.
- **Indexing:** The inverted index structure is a dictionary that stores each token and a list of document IDs in which the token appears. The program takes a document and starts adding the document ID for each token within that doc.
- **Retrieval & Ranking:** The cosine similarity ranking method determines how similar the query and the document are by comparing their vectors

---

## 5. Vocabulary Statistics
- **Vocabulary Size:** 30980
- **Sample of 100 Tokens:** ['fmd', 'alcoholinduc', 'pressureoverload', 'rela', 'oligo', 'stanc', 'buyin', 'stereoisom', 'intradur', 'caudat', 'crcscs', 'pudefici', 'tast', 'dyt', 'redifferenti', 'drugadr', 'receptorhsp', 'transduct', 'cultureadapt', 'vacuol', 'phosphotyrosin', 'sodium', 'fluorodeoxyglucos', 'quadruplex', 'tsce', 'leukemiainiti', 'hypercalcem', 'femal', 'czechoslovakia', 'lessen', 'statur', 'phenomena', 'lateact', 'auscultatori', 'hungri', 'pomb', 'disproport', 'globus', 'cucumerina', 'subscriptionbas', 'cilengitid', 'hivseroposit', 'disclos', 'function', 'autophagydefici', 'ltd', 'nhejdepend', 'tumordriven', 'substratum', 'substantia', 'offici', 'ethnicityspecif', 'plu', 'tsctic', 'intract', 'bordetella', 'estron', 'selfassess', 'tmposit', 'ppilik', 'gabpba', 'endosteallin', 'fifteen', 'core', 'nfκbdepend', 'learn', 'pacapspecif', 'contextur', 'reductionoxid', 'oliguria', 'cfainduc', 'vecadherin', 'hivneg', 'abstractmicrorna', 'eufa', 'oscillometr', 'anthropomorph', 'retroperiton', 'scbvkaiyuan', 'dextran', 'account', 'restitut', 'cancerrecruit', 'codomin', 'hcmvpermiss', 'japonica', 'northeastern', 'zfns', 'anyth', 'eprostanoid', 'blastema', 'anticitrullin', 'spore', 'blooddifferenti', 'lymphotoxinalphabeta', 'endothelialhaematopoiet', 'sitedepend', 'adher', 'insitu', 'fecund']

---

## 6. Query Results & Discussion
- **First 10 Answers for First 2 Queries:**
- - 1 Q0 31715818 1 0.9826 run_31715818_exact
- 1 Q0 1848452 2 0.2338 run_31715818_exact
- 1 Q0 169264 3 0.2258 run_31715818_exact
- 1 Q0 502797 4 0.2161 run_31715818_exact
- 1 Q0 17327939 5 0.2146 run_31715818_exact
- 1 Q0 8891333 6 0.2082 run_31715818_exact
- 1 Q0 9988425 7 0.1881 run_31715818_exact
- 1 Q0 11360430 8 0.1876 run_31715818_exact
- 1 Q0 8318286 9 0.1858 run_31715818_exact
- 1 Q0 5567223 10 0.1847 run_31715818_exact
- 3 Q0 14717500 1 0.9001 run_14717500_exact
- 3 Q0 15155862 2 0.3021 run_14717500_exact
- 3 Q0 23389795 3 0.2811 run_14717500_exact
- 3 Q0 2739854 4 0.2520 run_14717500_exact
- 3 Q0 4632921 5 0.1981 run_14717500_exact
- 3 Q0 2485101 6 0.1888 run_14717500_exact
- 3 Q0 24144677 7 0.1736 run_14717500_exact
- 3 Q0 15663829 8 0.1696 run_14717500_exact
- 3 Q0 9196472 9 0.1689 run_14717500_exact
- 3 Q0 22067786 10 0.1682 run_14717500_exact
- **Discussion:** The results of the full-text queries always had higher scores at the same ranking however they would result in an almost completely different ranking with most entries in the top 10 from a title-only query ranking significantly lower on a full-text query if the rank at all.

---

## 7. Mean Average Precision (MAP) Score
(Present MAP score computed using `trec_eval` and interpret the results.)

---

## 8. Conclusion
(Summarize key findings, possible improvements, and reflections on system performance.)
We found that overall a full-text query was more effective than a title-only query.
