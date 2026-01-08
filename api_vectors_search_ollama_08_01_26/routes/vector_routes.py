from fastapi import APIRouter
import os
from fastapi import UploadFile,File
from dotenv import load_dotenv
from models.vector import VectorDocs,VectorQuery
from services.vector_services import add_vector,search_vector,result
from utils.pdf_loader import load_pdf
from utils.chunker import chunk_text

load_dotenv()
router=APIRouter()

#HOME
@router.get("/")
def welcome():
    return {"message":"Welcome to Vector Task Day2!"}

#Query
@router.post("/upload-pdf")
async def store_docs(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        return {"error":"Invalid file format. Please upload a PDF file"}
    
    file_location=f"temp_files/{file.filename}"
    with open(file_location,"wb") as buffer:
        buffer.write(await file.read())

    text=load_pdf(file_location)
    chunks=chunk_text(text)
    for chunk in chunks:
        await add_vector(chunk,"document")
           
    return {"status":"Document stored successfully"}

@router.post("/vector-query")
async def search_query(q:VectorQuery, limit:int=3):
    query=q.query
    await add_vector(query,"query")

    search_result=await search_vector(query,limit)

    return await result(search_result,query)




    
