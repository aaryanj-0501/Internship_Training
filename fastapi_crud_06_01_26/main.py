from fastapi import FastAPI
from routes.note import router

app=FastAPI(title="FASTAPI MongoDB CURD")

app.include_router(router)