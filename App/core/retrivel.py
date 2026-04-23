# App/core/retrivel.py
import os
import json
from App.core.vector_storage import VectorStorage
from App.core.embeddings import get_embeddings
from App.core.config import DATA_PATH, INDEX_PATH
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def retrieve(query, top_k=5):
    # Load FAQs
    with open(DATA_PATH, 'r') as f:
        faqs = json.load(f)

    # Load the saved index
    vector_storage = VectorStorage(dim=384)
    vector_storage.load(INDEX_PATH)

    # Search
    query_vector = get_embeddings(query)
    indices = vector_storage.search(query_vector, top_k)
    results = [faqs[i] for i in indices]
    return results