from fastapi import FastAPI

from app.config import setup_database
from app.controller import book_router
from app.consumer import setup_consumer
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # atau ["*"] untuk semua origin (testing)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(book_router)

setup_consumer(app)

setup_database(app)
