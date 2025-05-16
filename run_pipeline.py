

from models.preprocessing import preprocess_and_save
from utils.build_index import build_index

MONGO_URI = 'mongodb://localhost:27017/'
DB_NAME = 'airbnbDB'
COLLECTION_NAME = 'listings'
CLEANED_PATH = 'processed/cleaned_text.txt'
VECTORS_PATH = 'processed/vectors.pkl'
INDEX_PATH = 'processed/index.faiss'

def main():
    print("[1/2] Preprocessing MongoDB data...")
    preprocess_and_save(MONGO_URI, DB_NAME, COLLECTION_NAME, CLEANED_PATH)

    print("[2/2] Building FAISS index...")
    build_index(CLEANED_PATH, VECTORS_PATH, INDEX_PATH)

    print("✅ Pipeline complete. You can now run chatbot.py")

if __name__ == "__main__":
    main()