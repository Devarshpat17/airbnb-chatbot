from pymongo import MongoClient

def get_collection(uri: str, db_name: str, collection_name: str):
    """
    Connect to MongoDB and return a collection handle.
    """
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        # Trigger server selection to verify connection
        client.admin.command('ping')
        db = client[db_name]
        return db[collection_name]
    except Exception as e:
        raise ConnectionError(f"Could not connect to MongoDB: {e}")

# Example usage
MONGO_URI = 'mongodb://localhost:27017/'
DB_NAME = 'airbnbDB'
COLLECTION_NAME = 'listings'

if __name__ == "__main__":
    try:
        collection = get_collection(MONGO_URI, DB_NAME, COLLECTION_NAME)
        print(f"✅ Connected to collection: {collection.full_name}")
    except ConnectionError as e:
        print(f"❌ {e}")
