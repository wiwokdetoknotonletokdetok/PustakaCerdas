from typing import Optional, List

from pydantic import BaseModel


class UserPayload(BaseModel):
    short_term_ids: Optional[List[str]] = None
