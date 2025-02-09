import json
import math
import os
from collections import defaultdict
from preprocess import Preprocessor

class Indexer:
    def __init__(self):
        self.inverted_index = defaultdict(dict)
        self.doc_lengths = {}