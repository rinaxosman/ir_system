import json
import numpy as np
import re
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
    text = text.lower()  # Lowercase
    text = re.sub(r'\W+', ' ', text)  # Remove special characters
    tokens = text.split()  # Tokenization
    tokens = [stemmer.stem(word) for word in tokens if word not in stop_words]  # Remove stopwords & stem
    return " ".join(tokens)

inverted_index_path = "data/scifact/inverted_index.json"
preprocessed_corpus_path = "data/scifact/preprocessed_corpus.json"

with open(preprocessed_corpus_path, 'r', encoding='utf-8') as f:
    preprocessed_corpus = json.load(f)

# Convertinto doc list
documents = {doc["doc_id"]: " ".join(doc["tokens"]) for doc in preprocessed_corpus}

doc_ids = list(documents.keys())
doc_texts = list(documents.values())

# ITF-IDF Vectorizer
vectorizer = TfidfVectorizer()
doc_vectors = vectorizer.fit_transform(doc_texts) 

def retrieve_and_rank(query, query_id, run_name, top_k=10):
    """ Retrieve and rank documents based on cosine similarity."""
    query = preprocess_text(query)  # Preprocess query like the corpus
    query_vector = vectorizer.transform([query])  # Conver into a TF-IDF vector
    similarities = cosine_similarity(query_vector, doc_vectors)[0]  # Compute cosine similarity

    # Ranksthe documents by theire similarity score
    ranked_docs = sorted(zip(doc_ids, similarities), key=lambda x: x[1], reverse=True)[:top_k]

    # Format results
    results = []
    for rank, (doc_id, score) in enumerate(ranked_docs, start=1):
        results.append(f"{query_id} Q0 {doc_id} {rank} {score:.4f} {run_name}")
        
    results.append("-----------")

    return results

# Test queries
test_queries = {
    1: {
        "query": "Nanotechnologies are emerging platforms that could be useful in measuring, understanding, and manipulating stem cells. Examples include magnetic nanoparticles and quantum dots for stem cell labeling and in vivo tracking; nanoparticles, carbon nanotubes, and polyplexes for the intracellular delivery of genes/oligonucleotides and protein/peptides; and engineered nanometer-scale scaffolds for stem cell differentiation and transplantation. This review examines the use of nanotechnologies for stem cell tracking, differentiation, and transplantation. We further discuss their utility and the potential concerns regarding their cytotoxicity.",
        "run_name": "run_31715818_exact"
    },
    3: {
        "query": "Genome-wide association studies (GWAS) have now identified at least 2,000 common variants that appear associated with common diseases or related traits (http://www.genome.gov/gwastudies), hundreds of which have been convincingly replicated. It is generally thought that the associated markers reflect the effect of a nearby common (minor allele frequency >0.05) causal site, which is associated with the marker, leading to extensive resequencing efforts to find causal sites. We propose as an alternative explanation that variants much less common than the associated one may create 'synthetic associations' by occurring, stochastically, more often in association with one of the alleles at the common site versus the other allele. Although synthetic associations are an obvious theoretical possibility, they have never been systematically explored as a possible explanation for GWAS findings. Here, we use simple computer simulations to show the conditions under which such synthetic associations will arise and how they may be recognized. We show that they are not only possible, but inevitable, and that under simple but reasonable genetic models, they are likely to account for or contribute to many of the recently identified signals reported in genome-wide association studies. We also illustrate the behavior of synthetic associations in real datasets by showing that rare causal mutations responsible for both hearing loss and sickle cell anemia create genome-wide significant synthetic associations, in the latter case extending over a 2.5-Mb interval encompassing scores of 'blocks' of associated variants. In conclusion, uncommon or rare genetic variants can easily create synthetic associations that are credited to common variants, and this possibility requires careful consideration in the interpretation and follow up of GWAS signals.",
        "run_name": "run_14717500_exact"
    },
    5: {
        "query": "OBJECTIVES To carry out a further survey of archived appendix samples to understand better the differences between existing estimates of the prevalence of subclinical infection with prions after the bovine spongiform encephalopathy epizootic and to see whether a broader birth cohort was affected, and to understand better the implications for the management of blood and blood products and for the handling of surgical instruments. DESIGN Irreversibly unlinked and anonymised large scale survey of archived appendix samples. SETTING Archived appendix samples from the pathology departments of 41 UK hospitals participating in the earlier survey, and additional hospitals in regions with lower levels of participation in that survey. SAMPLE 32,441 archived appendix samples fixed in formalin and embedded in paraffin and tested for the presence of abnormal prion protein (PrP). RESULTS Of the 32,441 appendix samples 16 were positive for abnormal PrP, indicating an overall prevalence of 493 per million population (95% confidence interval 282 to 801 per million). The prevalence in those born in 1941-60 (733 per million, 269 to 1596 per million) did not differ significantly from those born between 1961 and 1985 (412 per million, 198 to 758 per million) and was similar in both sexes and across the three broad geographical areas sampled. Genetic testing of the positive specimens for the genotype at PRNP codon 129 revealed a high proportion that were valine homozygous compared with the frequency in the normal population, and in stark contrast with confirmed clinical cases of vCJD, all of which were methionine homozygous at PRNP codon 129. CONCLUSIONS This study corroborates previous studies and suggests a high prevalence of infection with abnormal PrP, indicating vCJD carrier status in the population compared with the 177 vCJD cases to date. These findings have important implications for the management of blood and blood products and for the handling of surgical instruments.",
        "run_name": "run_13734012_exact"
    }
}
all_results = []
for query_id, data in test_queries.items():
    all_results.extend(retrieve_and_rank(data["query"], query_id, data["run_name"]))

# Save results
results_path = "results/Results.txt"
with open(results_path, "w", encoding="utf-8") as f:  
    f.write("\n".join(all_results) + "\n")

print(f"✅ Results appended to {results_path}")
