import os
import json
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

nltk.download("punkt")
nltk.download("stopwords")

class Preprocessor:
    def __init__(self, stopwords_file=None, use_stemming=True):
        self.use_stemming = use_stemming

        # Automatically determine the correct path to StopWords.txt
        if stopwords_file is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of preprocess.py
            stopwords_file = os.path.join(base_dir, "..", "data", "scifact", "StopWords.txt")

        # Load stopwords from file
        if os.path.exists(stopwords_file):
            with open(stopwords_file, "r", encoding="utf-8") as f:
                self.stopwords = set(f.read().splitlines())
        else:
            raise FileNotFoundError(f"Stopwords file not found: {stopwords_file}")

        self.stemmer = PorterStemmer()

    def preprocess_text(self, text):
        tokens = word_tokenize(text.lower())
        tokens = [re.sub(r'\W+', '', token) for token in tokens if token.isalpha()]
        tokens = [token for token in tokens if token not in self.stopwords]
        if self.use_stemming:
            tokens = [self.stemmer.stem(token) for token in tokens]
        return tokens

    def preprocess_corpus(self, corpus_path=None):
        if corpus_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            corpus_path = os.path.join(base_dir, "..", "data", "scifact", "corpus.jsonl")

        corpus = []
        if os.path.exists(corpus_path):
            with open(corpus_path, "r", encoding="utf-8") as f:
                for line in f:
                    doc = json.loads(line)
                    doc_id = doc.get("doc_id", "")
                    text = doc.get("abstract", "")
                    tokens = self.preprocess_text(text)
                    corpus.append((doc_id, tokens))
        else:
            raise FileNotFoundError(f"Corpus file not found: {corpus_path}")

        return corpus