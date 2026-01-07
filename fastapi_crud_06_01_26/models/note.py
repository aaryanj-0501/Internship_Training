from pydantic import BaseModel,EmailStr

class Note(BaseModel):
    name: str
    email: EmailStr
    age: int
    title: str
    desc: str
    important: bool=None
