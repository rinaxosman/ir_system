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

    python src/top_2_sample.py

Top 10 Results for First 2 Queries (Title-Only Retrieval)

Query ID: 1
1 Q0 31715818 1 1.0000 run_31715818_title
1 Q0 5415832 2 0.2493 run_31715818_title
1 Q0 87430549 3 0.2121 run_31715818_title
1 Q0 29321530 4 0.2110 run_31715818_title
1 Q0 41782935 5 0.1914 run_31715818_title
1 Q0 123859 6 0.1892 run_31715818_title
1 Q0 20186814 7 0.1787 run_31715818_title
1 Q0 20532591 8 0.1739 run_31715818_title
1 Q0 6955746 9 0.1703 run_31715818_title
1 Q0 24766509 10 0.1701 run_31715818_title
Query ID: 3
3 Q0 14717500 1 1.0000 run_14717500_title
3 Q0 24530130 2 0.3664 run_14717500_title
3 Q0 25643818 3 0.3477 run_14717500_title
3 Q0 2739854 4 0.3379 run_14717500_title
3 Q0 13777706 5 0.3284 run_14717500_title
3 Q0 2095573 6 0.2864 run_14717500_title
3 Q0 23389795 7 0.2848 run_14717500_title
3 Q0 15155862 8 0.2434 run_14717500_title
3 Q0 4421746 9 0.2430 run_14717500_title
3 Q0 16691520 10 0.2396 run_14717500_title

Top 10 Results for First 2 Queries (Title + Full Text Retrieval)

Query ID: 1
1 Q0 31715818 1 1.0000 run_31715818_text
1 Q0 502797 2 0.2538 run_31715818_text
1 Q0 1848452 3 0.2374 run_31715818_text
1 Q0 87430549 4 0.2306 run_31715818_text
1 Q0 8891333 5 0.2251 run_31715818_text
1 Q0 5567223 6 0.1922 run_31715818_text
1 Q0 169264 7 0.1917 run_31715818_text
1 Q0 86129154 8 0.1914 run_31715818_text
1 Q0 4457834 9 0.1896 run_31715818_text
1 Q0 8318286 10 0.1874 run_31715818_text
Query ID: 3
3 Q0 14717500 1 0.9885 run_14717500_text
3 Q0 23389795 2 0.3357 run_14717500_text
3 Q0 2739854 3 0.3051 run_14717500_text
3 Q0 2485101 4 0.2934 run_14717500_text
3 Q0 15155862 5 0.2849 run_14717500_text
3 Q0 4632921 6 0.1930 run_14717500_text
3 Q0 23686039 7 0.1772 run_14717500_text
3 Q0 9196472 8 0.1767 run_14717500_text
3 Q0 13373629 9 0.1728 run_14717500_text
3 Q0 11532028 10 0.1636 run_14717500_text


- **Discussion:** The results of the full-text queries always had higher scores at the same ranking however they would result in an almost completely different ranking with most entries in the top 10 from a title only query ranking significantly lower on a full-text query if the rank at all.
- The results, saved in 2_sample_queries.txt, were generated using top_2_sample.py. In both title-only and title + full-text retrieval, the top-ranked document is always an exact match with a score of 1.0000. This makes sense because the query directly matches an existing document in the dataset.
- However, the order of the remaining documents changes between the two methods. Title-only retrieval ranks documents based on how similar their titles are to the query, prioritizing those with closely matching titles. Title + full-text retrieval, on the other hand, considers the entire content, which can cause documents with relevant text (but different titles) to rank higher.
- Title-only retrieval is more precise because it retrieves documents with strong title similarity, but it may miss relevant content that doesn’t have a matching title. Title + full-text retrieval improves recall by finding documents where the query terms appear anywhere in the text, but this can also lead to some less relevant documents ranking higher.

---

## 7. Mean Average Precision (MAP) Score
(Present MAP score computed using `trec_eval` and interpret the results.)

---

## 8. Conclusion
(Summarize key findings, possible improvements, and reflections on system performance.)
We found that overall a full-text query was more effective than a title-only query.
