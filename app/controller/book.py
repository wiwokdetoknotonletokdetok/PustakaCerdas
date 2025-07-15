from fastapi import APIRouter, Query

from app.dto import WebResponse
from app.services import search_book

router = APIRouter()


@router.get("/books")
def get_books(q: str = Query(None)):
    response = WebResponse.builder().data(search_book(q)).build()
    return response.dict()
