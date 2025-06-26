from typing import Optional, TypeVar, Generic

from pydantic import BaseModel

T = TypeVar("T")


class WebResponse(BaseModel, Generic[T]):
    data: Optional[T] = None
    errors: Optional[str] = None

    @classmethod
    def builder(cls) -> "WebResponseBuilder[T]":
        return WebResponseBuilder()

    def dict(self, *args, **kwargs):
        kwargs.setdefault("exclude_none", True)
        return super().dict(*args, **kwargs)


class WebResponseBuilder(Generic[T]):
    def __init__(self):
        self._data: Optional[T] = None
        self._errors: Optional[str] = None

    def data(self, data: T) -> "WebResponseBuilder":
        self._data = data
        return self

    def errors(self, error: str) -> "WebResponseBuilder":
        self._errors = error
        return self

    def build(self) -> WebResponse[T]:
        return WebResponse(data=self._data, errors=self._errors)
