import os
import pickle
from models import search, response_generator

def chatbot():
    print("MongoDB Chatbot. Type 'exit' to quit.")
    while True:
        q = input("\nYou: ")
        if q.lower() in ["exit", "quit"]:
            break
        results = search.search(q, 'processed/index.faiss', 'processed/vectors.pkl')
        response = response_generator.generate_response(results, q)
        print("Bot:", response)

if __name__ == '__main__':
    chatbot()
