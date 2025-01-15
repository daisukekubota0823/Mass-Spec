# app/main.py

from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="Python-R Integration API")

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Python-R Integration API"}
