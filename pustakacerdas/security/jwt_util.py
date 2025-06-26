import jwt

from pustakacerdas.config import Config


def decode_jwt(token):
    try:
        payload = jwt.decode(token, Config.JWT_SECRET, algorithms=[Config.JWT_ALGORITHM])
        return payload
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None
