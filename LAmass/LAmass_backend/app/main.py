from fastapi import FastAPI
from app.routes import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Python + R Integration API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace '*' with your specific frontend domain for better security
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)
app.include_router(router)