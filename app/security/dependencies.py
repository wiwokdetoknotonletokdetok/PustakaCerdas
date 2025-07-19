from typing import Optional

from fastapi import Header

from app.security.jwt_util import jwt_decode


async def get_user_id_from_token(authorization: Optional[str] = Header(default=None)) -> Optional[str]:
    if not authorization or not authorization.startswith("Bearer "):
        return None

    token = authorization[len("Bearer "):]
    payload = jwt_decode(token)
    if not payload:
        return None

    return payload.get("sub")
