from fastapi import APIRouter
import ollama
import os
import uuid
from models.vector import VectorDocs,VectorQuery
from config.db import client

router=APIRouter()
embed_model=os.getenv("EMBED_MODEL")

#HOME
@router.get("/")
def welcome():
    return {"message":"Welcome to Vector Task Day2!"}

def get_embedding(text:str):
    response=ollama.embeddings(
        model='nomic-embed-text',
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

#Query
@router.post("/vector-doc")
async def store_docs(document:VectorDocs):
    doc=document.docs
    
    client.upsert(
        collection_name='vector_crud',
        points=[build_point(doc)]
    )

    return {"status":"Document stored successfully"}

@router.post("/vector-query")
async def search_query(q:VectorQuery, limit:int=3):
    query=q.query
    point=build_point(query)
    client.upsert(
        collection_name='queries',
        points=[point]
    )

    search_result=client.query_points(
        collection_name='vector_crud',
        query=get_embedding(query),
        limit=limit,
        with_payload=True
    )

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




    
