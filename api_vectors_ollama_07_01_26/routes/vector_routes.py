from fastapi import APIRouter
import os
from dotenv import load_dotenv
from models.vector import VectorDocs,VectorQuery
from services.vector_services import add_vector,search_vector,result

load_dotenv()
router=APIRouter()

#HOME
@router.get("/")
def welcome():
    return {"message":"Welcome to Vector Task Day2!"}

#Query
@router.post("/vector-doc")
async def store_docs(document:VectorDocs):
    await add_vector(document.docs,"document")

    return {"status":"Document stored successfully"}

@router.post("/vector-query")
async def search_query(q:VectorQuery, limit:int=3):
    query=q.query
    await add_vector(query,"query")

    search_result=await search_vector(query,limit)

    return await result(search_result,query)




    
