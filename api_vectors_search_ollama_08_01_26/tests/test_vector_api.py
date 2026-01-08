import requests

from dotenv import load_dotenv
import os

load_dotenv()
BASE_URL=os.getenv("BASE_URL")

def test_store_docs():
    url=f"{BASE_URL}/upload-pdf"
    payload={
        "docs":"RAG combines retrieval with generation using vector databases."
    }

    response=requests.post(url,json=payload)
    print("Stores document response:",response.status_code+" "+response.json())

def test_search_query():
    url=f"{BASE_URL}/vector-query?limit=3"
    payload={
        "query":"What is RAG?"
    }

    response=requests.post(url,json=payload)
    print("Search query response:",response.status_code+" "+response.json())

if __name__=="__main__":
    print("Running Tests...")
    test_store_docs()
    test_search_query()
    print("Tests Completed.")