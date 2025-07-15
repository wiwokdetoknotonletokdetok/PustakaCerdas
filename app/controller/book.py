from fastapi import APIRouter, Query

from app.dto import WebResponse
from app.services import search_book

router = APIRouter()


@router.get("/books")
def get_books(q: str = Query(None), max: int = Query(None), threshold: float = Query(None)):
    response = WebResponse.builder().data(search_book(q, max, threshold)).build()
    return response.dict()
