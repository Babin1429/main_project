import numpy as np
import os
try:
    import faiss
except ImportError as e:
    print(f"Error importing faiss: {e}")
    faiss = None

class VectorStorage:
    def __init__(self, dim):
        if faiss is None:
            raise RuntimeError("faiss not available")
        self.index = faiss.IndexFlatL2(dim)

    def add(self, vectors):
        self.index.add(np.array(vectors).astype('float32'))

    def search(self, query_vector, top_k=5):
        distances, indices = self.index.search(
            np.array([query_vector]).astype('float32'), top_k
        )
        return indices[0]

    def save(self, file_path):
        faiss.write_index(self.index, file_path)

    def load(self, file_path):
        if os.path.exists(file_path):
            self.index = faiss.read_index(file_path)
        else:
            raise FileNotFoundError(f"Index file {file_path} not found.")