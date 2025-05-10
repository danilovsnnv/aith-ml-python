from jose import JWTError, jwt

from core.config import settings


def verify_access_token(token: str) -> dict:
    """
    Decodes JWT token using the public key from settings and returns its payload.
    Raises an exception if verification fails.
    """
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
    except JWTError as e:
        raise e
    return payload
