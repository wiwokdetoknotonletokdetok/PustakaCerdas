from functools import wraps

from flask import request

from app.dto.web_response import WebResponse
from app.security.jwt_util import decode_jwt


def allowed_roles(roles):
    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get("Authorization", "")
            token = None
            if auth_header.startswith("Bearer "):
                token = auth_header[len("Bearer "):]

            if not token:
                response = WebResponse.builder().errors("Unauthorized").build()
                return response.dict(), 401

            payload = decode_jwt(token)
            if not payload:
                response = WebResponse.builder().errors("Invalid token").build()
                return response.dict(), 401

            user_role = payload.get("role")
            if user_role not in roles:
                response = WebResponse.builder().errors("Forbidden").build()
                return response.dict(), 403

            return func(*args, payload=payload, **kwargs)

        return wrapper

    return decorator
