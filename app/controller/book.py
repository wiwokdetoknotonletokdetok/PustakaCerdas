from app.dto import WebResponse
from fastapi import APIRouter

router = APIRouter()


@router.get("/books")
def get_books():
    response = WebResponse.builder().data("OK").build()
    return response.dict()
