from fastapi import APIRouter, Query

from app.dto import WebResponse
from app.services import get_book_recommendations

router = APIRouter()


@router.get("/recommendations/books")
def get_books_recommendations(userId: str = Query(None), limit: int = Query(5)):
    recommendations = get_book_recommendations(userId, limit)
    response = WebResponse.builder().data(recommendations).build()
    return response.dict()
