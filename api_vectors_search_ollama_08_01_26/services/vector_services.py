import ollama
import uuid
from config.db import client
import os
from dotenv import load_dotenv
from typing import Optional
import json

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
            "text": text,
            "source":"pdf"
        }
    })

async def add_vector(text:str,type:str):
    client.upsert(
        collection_name=(collection_docs if type=="document" else collection_queries),
        points=[build_point(text)]
    )

async def search_vector(query:str,top:int):
    embedding=get_embedding(query)
    return client.query_points(
        collection_name=collection_docs,
        query=embedding,
        limit=top,
        with_payload=["text","source"],
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

def export_collection_to_json(collection_name:str,output_file:str="exported_collection.json"):
    all_points=[]
    offset:Optional[str]=None
    
    while True:
        points,offset=client.scroll(
            collection_name=collection_name,
            limit=100,
            offset=offset,
            with_payload=True
        )

        for point in points:
            all_points.append({
                "id":point.id,
                "payload":point.payload
            })
        if offset is None:
            break

    with open(output_file,"w",encoding="utf-8") as f:
        json.dump(all_points,f,ensure_ascii=False,indent=2)
