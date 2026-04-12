from sentence_transformers import SentenceTransformer

try:
    model = SentenceTransformer('all-MiniLM-L6-v2')
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

def get_embeddings(text):
    if model is None:
        raise RuntimeError("Model not loaded")
    return model.encode(text)