

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from App.core.embeddings import get_embeddings
from App.core.vector_storage import VectorStorage
from App.core.config import DATA_PATH, INDEX_PATH

with open(DATA_PATH, 'r') as f:
    faqs = json.load(f)

texts = [faq["question"] for faq in faqs]
vectors = [get_embeddings(text) for text in texts]

dim = len(vectors[0])
Vector_storage = VectorStorage(dim)
Vector_storage.add(vectors)
Vector_storage.save(INDEX_PATH)

print("Index built and saved successfully.")