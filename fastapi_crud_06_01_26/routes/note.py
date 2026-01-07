from fastapi import APIRouter, HTTPException
from models.note import Note
from schemas.note import noteEntity
from config.db import collection
from bson import ObjectId

router= APIRouter()

#HOME
@router.get("/")
def welcome():
    return {"message":"Welcome! Add Your Notes"}

#CREATE
@router.post("/note")
async def add_note(note:Note):
    new_note=await collection.insert_one(note.dict())
    created=await collection.find_one({"_id":new_note.inserted_id})
    return noteEntity(created)

#READ ALL
@router.get("/notes")
async def get_all_notes():
    notes=[]
    async for note in collection.find():
        notes.append(noteEntity(note))
    return notes

#READ ONE
@router.get("/note/{note_id}")
async def get_note(note_id:str):
    note=await collection.find_one({"_id":ObjectId(note_id)})
    if not note:
        raise HTTPException(404,"User Not Found")
    return noteEntity(note)

#UPDATE ONE
@router.put("/note/{note_id}")
async def update_note(note_id:str,note:Note):
    updated_note=await collection.find_one_and_update(
        {"_id":ObjectId(note_id)},
        {"$set":dict(note)}
    )
    if updated_note is None:
        raise HTTPException(404,"User Not Found")
    return noteEntity(updated_note)

#DELETE A Note
@router.delete("/note/{note_id}")
async def delete_note(note_id:str):
    deleted=await collection.find_one_and_delete({"_id":ObjectId(note_id)})
    if deleted is None:
        raise HTTPException(404,"User Not Found")
    return {"message":"User deleted Successfully"}



