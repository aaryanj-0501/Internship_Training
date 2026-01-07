from motor.motor_asyncio import AsyncIOMotorClient
import os

mongo_uri=os.getenv("MONGO_URI")

client = AsyncIOMotorClient(mongo_uri)
database=client.crud_fastapi
collection=database.notes

