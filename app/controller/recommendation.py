from typing import Optional

from fastapi import APIRouter, Query, Depends
from fastapi.responses import JSONResponse

from app.dto import WebResponse
from app.security import get_user_id_from_token
from app.services import get_book_recommendations, init_user_embedding

router = APIRouter()


@router.get("/recommendations/books")
def get_books_recommendations(limit: int = Query(5), user_id: Optional[str] = Depends(get_user_id_from_token)):
    recommendations = get_book_recommendations(user_id, limit)
    response = WebResponse.builder().data(recommendations).build()
    return JSONResponse(status_code=200, content=response.dict())


@router.delete("/recommendations/books/reset")
def reset_books_recommendations(user_id: Optional[str] = Depends(get_user_id_from_token)):
    if not user_id:
        response = WebResponse.builder().errors("Unauthorized").build()
        return JSONResponse(status_code=401, content=response.dict())
    else:
        init_user_embedding(user_id)
        response = WebResponse.builder().data("OK").build()
        return JSONResponse(status_code=200, content=response.dict())
