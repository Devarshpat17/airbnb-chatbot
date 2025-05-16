import json
import pickle
import faiss
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

def build_embeddings(texts):
    return model.encode(texts, convert_to_numpy=True)

def search(query, index_path, vectors_path, top_k=3):
    index = faiss.read_index(index_path)
    with open(vectors_path, 'rb') as f:
        meta = pickle.load(f)

    query_vec = model.encode([query])
    D, I = index.search(query_vec, top_k)
    return [meta[i] for i in I[0]]
