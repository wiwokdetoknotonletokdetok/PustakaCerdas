from fastapi import APIRouter

from app.dto import WebResponse

router = APIRouter()


@router.get("/books")
def get_books():
    response = WebResponse.builder().data("OK").build()
    return response.dict()
