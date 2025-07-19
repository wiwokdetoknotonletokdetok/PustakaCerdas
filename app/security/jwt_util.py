import jwt

from app.config import settings


def jwt_decode(token):
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        return payload
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None
