from pydantic import BaseModel

class VectorQuery(BaseModel):
    query:str

class VectorDocs(BaseModel):
    docs:str
