import secrets

from fastapi import Header, HTTPException, status

from config import settings


async def check_api_key(
    x_api_key: str = Header(None, alias="X-API-Key"),
) -> str:
    """Validate the X-API-Key header against the configured secret.

    A constant-time comparison is used to avoid timing attacks.
    """
    if x_api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key. Provide it via the X-API-Key header.",
        )
    if not secrets.compare_digest(x_api_key, settings.api_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )
    return x_api_key