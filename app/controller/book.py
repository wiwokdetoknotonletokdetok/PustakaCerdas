from fastapi import APIRouter, Query

from app.dto import WebResponse
from app.services.embedding_service import get_query_embedding

router = APIRouter()


@router.get("/books")
def get_books(q: str = Query(None)):
    vector = get_query_embedding(q)
    response = WebResponse.builder().data(vector).build()
    return response.dict()
