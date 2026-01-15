import os
import uuid
from dotenv import load_dotenv
from config.qdrant import client
from utils.embeddings import get_embedding
from utils.chunker import clean_text,chunk_text
from utils import pdf_loader
from services.query_retriever import get_query_retriever
from services.generate_metadata import infer_policy_type,infer_section,infer_location,infer_employee_type
from services.final_result import extract_context,clean_output,answer_chain
import logging

load_dotenv()
collection_handbook=os.getenv("QDRANT_COLLECTION")

def add_vectors(chunks:str):
    points=[]
    logging.info("Adding vectors to Qdrant collection.")
    for chunk in chunks:
        clean_chunk=clean_text(chunk)
        embedding=get_embedding(clean_chunk)
        points.append({
            "id":str(uuid.uuid4()),
            "vector":embedding,
            "payload":{
                "text":clean_chunk,
                "source":"employee_handbook",
                "policy_type":infer_policy_type(clean_chunk),
                "section":infer_section(clean_chunk),
                "location":infer_location(clean_chunk),
                "employee_type":infer_employee_type(clean_chunk)
            }
        })
    print(f"Chunk added:",len(points))
    client.upsert(
        collection_name=collection_handbook,
        points=points
    )
    print("Vectors added successfully.")
    logging.info("Vectors added successfully.")

def get_result(query:str,limit:int=5):
    query_result=get_query_retriever(query,limit)
    print(len(query_result))
    context=extract_context(query_result)
    response=answer_chain.run(question=query,context=context)
    return clean_output(response)

async def process_handbook(file):
    if not file.filename.endswith(".pdf"):
        raise ValueError("Invalid file format. Please upload a PDF file")
    
    file_location=f"temp_files/{file.filename}"
    with open(file_location,"wb") as buffer:
        buffer.write(await file.read())

    print("File saved")
    text=pdf_loader.load_pdf(file_location)
    chunks=chunk_text(text)
    print(f"Total chunks created:{len(chunks)}")
    add_vectors(chunks)

    print("status:Handbook processed and vectors added successfully")