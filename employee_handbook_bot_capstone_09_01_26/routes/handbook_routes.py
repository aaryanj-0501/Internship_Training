from fastapi import APIRouter,UploadFile,File,BackgroundTasks
from services.handbook_services import process_handbook,get_result
from models.handbook_model import HandbookQuery  
import logging

router=APIRouter()
logger = logging.getLogger(__name__)

#HOME
@router.get("/")
def welcome():
    logger.info("Welcome test")
    return {"message":"Welcome to Employee Handbook Bot!"}

@router.post("/upload-handbook")
async def upload_handbook(file: UploadFile = File(...),background_tasks: BackgroundTasks=None):
    background_tasks.add_task(process_handbook,file)
    
    return {"status":"Handbook uploaded and processing started."}

@router.post("/chat")
def handbook_query(query:HandbookQuery, limit:int=5):
    query_text=query.question
    search_result=get_result(query_text,limit)
    return search_result

