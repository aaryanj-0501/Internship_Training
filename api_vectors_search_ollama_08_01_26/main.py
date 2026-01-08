from fastapi import FastAPI
from routes.vector_routes import router

app=FastAPI(title="VectorDB using Ollama and Qdrant")

app.include_router(router)