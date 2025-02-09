import json
import numpy as np
import re
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk

# Download NLTK stopwords if not available
nltk.download("stopwords")

# Initialize Stopwords and Stemmer
stop_words = set(stopwords.words("english"))
stemmer = PorterStemmer()

def preprocess_text(text):
    text = text.lower()  # Lowercase
    text = re.sub(r'\W+', ' ', text)  # Remove special characters
    tokens = text.split()  # Tokenization
    tokens = [stemmer.stem(word) for word in tokens if word not in stop_words]  # Remove stopwords & stem
    return " ".join(tokens)

inverted_index_path = "data\scifact\inverted_index.json"
preprocessed_corpus_path = "data\scifact\preprocessed_corpus.json"

# Load JSON files
with open(preprocessed_corpus_path, 'r', encoding='utf-8') as f:
    preprocessed_corpus = json.load(f)

# Convert corpus into doc list
documents = {doc["doc_id"]: " ".join(doc["tokens"]) for doc in preprocessed_corpus}

# list of document IDs and corresponding text
doc_ids = list(documents.keys())
doc_texts = list(documents.values())

# ITF-IDF Vectorizer
vectorizer = TfidfVectorizer()
doc_vectors = vectorizer.fit_transform(doc_texts) 

def retrieve_and_rank(query, query_id, top_k=10):
    """ Retrieve and rank documents based on cosine similarity."""
    query = preprocess_text(query)  # Preprocess query like the corpus
    query_vector = vectorizer.transform([query])  # Converts tghe query into TF-IDF vector
    similarities = cosine_similarity(query_vector, doc_vectors)[0]  # Compute cosine similarity

    # Rank documents by similarity score
    ranked_docs = sorted(zip(doc_ids, similarities), key=lambda x: x[1], reverse=True)[:top_k]

    # Formats 
    results = []
    for rank, (doc_id, score) in enumerate(ranked_docs, start=1):
        results.append(f"{query_id} Q0 {doc_id} {rank} {score:.4f} run_name")

    return results

test_queries = {
    1: "Selective control of receptor trafficking provides a mechanism for remodeling the receptor composition of excitatory synapses, and thus supports synaptic transmission, plasticity, and development. GluN3A (formerly NR3A) is a nonconventional member of the NMDA receptor (NMDAR) subunit family, which endows NMDAR channels with low calcium permeability and reduced magnesium sensitivity compared with NMDARs comprising only GluN1 and GluN2 subunits. Because of these special properties, GluN3A subunits act as a molecular brake to limit the plasticity and maturation of excitatory synapses, pointing toward GluN3A removal as a critical step in the development of neuronal circuitry. However, the molecular signals mediating GluN3A endocytic removal remain unclear. Here we define a novel endocytic motif (YWL), which is located within the cytoplasmic C-terminal tail of GluN3A and mediates its binding to the clathrin adaptor AP2. Alanine mutations within the GluN3A endocytic motif inhibited clathrin-dependent internalization and led to accumulation of GluN3A-containing NMDARs at the cell surface, whereas mimicking phosphorylation of the tyrosine residue promoted internalization and reduced cell-surface expression as shown by immunocytochemical and electrophysiological approaches in recombinant systems and rat neurons in primary culture. We further demonstrate that the tyrosine residue is phosphorylated by Src family kinases, and that Src-activation limits surface GluN3A expression in neurons. Together, our results identify a new molecular signal for GluN3A internalization that couples the functional surface expression of GluN3A-containing receptors to the phosphorylation state of GluN3A subunits, and provides a molecular framework for the regulation of NMDAR subunit composition with implications for synaptic plasticity and neurodevelopment.",
    2: "Alterations of the architecture of cerebral white matter in the developing human brain can affect cortical development and result in functional disabilities. A line scan diffusion-weighted magnetic resonance imaging (MRI) sequence with diffusion tensor analysis was applied to measure the apparent diffusion coefficient, to calculate relative anisotropy, and to delineate three-dimensional fiber architecture in cerebral white matter in preterm (n = 17) and full-term infants (n = 7). To assess effects of prematurity on cerebral white matter development, early gestation preterm infants (n = 10) were studied a second time at term. In the central white matter the mean apparent diffusion coefficient at 28 wk was high, 1.8 microm2/ms, and decreased toward term to 1.2 microm2/ms. In the posterior limb of the internal capsule, the mean apparent diffusion coefficients at both times were similar (1.2 versus 1.1 microm2/ms). Relative anisotropy was higher the closer birth was to term with greater absolute values in the internal capsule than in the central white matter. Preterm infants at term showed higher mean diffusion coefficients in the central white matter (1.4 +/- 0.24 versus 1.15 +/- 0.09 microm2/ms, p = 0.016) and lower relative anisotropy in both areas compared with full-term infants (white matter, 10.9 +/- 0.6 versus 22.9 +/- 3.0%, p = 0.001; internal capsule, 24.0 +/- 4.44 versus 33.1 +/- 0.6% p = 0.006). Nonmyelinated fibers in the corpus callosum were visible by diffusion tensor MRI as early as 28 wk; full-term and preterm infants at term showed marked differences in white matter fiber organization. The data indicate that quantitative assessment of water diffusion by diffusion tensor MRI provides insight into microstructural development in cerebral white matter in living infants."
}

# Generatest he results for all queries
all_results = []
for query_id, query_text in test_queries.items():
    all_results.extend(retrieve_and_rank(query_text, query_id))

results_path = "results\Results.txt"
with open(results_path, "w", encoding="utf-8") as f:
    f.write("\n".join(all_results))

print(f"✅ Results saved to {results_path}")
