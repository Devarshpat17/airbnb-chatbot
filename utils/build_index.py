import faiss
import json
import pickle
from models.search import build_embeddings

def build_index(cleaned_path, vec_out_path, index_out_path):
    texts = []
    data = []
    with open(cleaned_path, 'r') as f:
        for line in f:
            item = json.loads(line)
            texts.append(json.dumps(item["data"]))
            data.append(item)
    
    vectors = build_embeddings(texts)
    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors)
    faiss.write_index(index, index_out_path)

    with open(vec_out_path, 'wb') as f:
        pickle.dump(data, f)
