from fastapi import FastAPI

from app.controller import book_router

app = FastAPI()

app.include_router(book_router)
