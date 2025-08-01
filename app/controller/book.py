from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from app.dto import WebResponse
from app.services import search_book

router = APIRouter()


@router.get("/books")
def get_books(q: str = Query(None), limit: int = Query(5), threshold: float = Query(0.40)):
    response = WebResponse.builder().data(search_book(q, limit, threshold)).build()
    return JSONResponse(status_code=200, content=response.dict())
