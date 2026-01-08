import requests

from dotenv import load_dotenv
import os

load_dotenv()
BASE_URL=os.getenv("BASE_URL")
pdf_path="temp_files/sample.pdf"

def test_store_docs():
    if not os.path.exists(pdf_path):
        print("PDF file for testing not found.")
        return
    
    url=f"{BASE_URL}/upload-pdf"

    with open(pdf_path,"rb") as f:
        files={
            "file":("sample.pdf",f,"application/pdf")
        }
        response=requests.post(url,files=files)

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