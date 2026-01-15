from fastapi import FastAPI
from routes.handbook_routes import router
from starlette.middleware.cors import CORSMiddleware

app=FastAPI(title="Employee Handbook Bot")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)