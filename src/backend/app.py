from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import api_router
app = FastAPI(title="ELLP API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)
