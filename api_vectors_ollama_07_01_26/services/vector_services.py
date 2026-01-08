import ollama
import uuid
from config.db import client
import os
from dotenv import load_dotenv

load_dotenv()
embed_model=os.getenv("EMBED_MODEL")
collection_docs=os.getenv("COLLECTION_DOCS")
collection_queries=os.getenv("COLLECTION_QUERY")

def get_embedding(text:str):
    response=ollama.embeddings(
        model=embed_model,
        prompt=text,
    )

    return response["embedding"]

def build_point(text:str):
    embedding=get_embedding(text)

    return ({
        "id":str(uuid.uuid4()),
        "vector": embedding,
        "payload":{
            "text": text
        }
    })

async def add_vector(text:str,type:str):
    client.upsert(
        collection_name=(collection_docs if type=="document" else collection_queries),
        points=[build_point(text)]
    )

async def search_vector(query:str,limit:int):
    return client.query_points(
        collection_name=collection_docs,
        query=get_embedding(query),
        limit=limit,
        with_payload=True
    )

async def result(search_result,query:str):
    return {
        "query":query,
        "results":[
            {
                "id":point.id,
                "score":point.score,
                "payload":point.payload
            }
            for point in search_result.points
        ]
    }