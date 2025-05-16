import json
import datetime
from bson.decimal128 import Decimal128
from .mongo_connector import get_collection

def clean_document(doc):
    def recurse(d):
        if isinstance(d, dict):
            return {k: recurse(v) for k, v in d.items() if v not in [None, "", "unknown", 0]}
        elif isinstance(d, list):
            return [recurse(i) for i in d if i not in [None, "", "unknown", 0]]
        elif isinstance(d, datetime.datetime):
            return d.isoformat()
        elif isinstance(d, Decimal128):
            return float(d.to_decimal())  # <-- fix here
        return d

    return recurse(doc)

def preprocess_and_save(uri, db, col, out_path):
    collection = get_collection(uri, db, col)
    with open(out_path, "w") as f:
        for doc in collection.find():
            cleaned = clean_document(doc)
            f.write(json.dumps({"_id": str(doc.get("_id")), "data": cleaned}) + "\n")
    print(f"Preprocessed data saved to {out_path}")