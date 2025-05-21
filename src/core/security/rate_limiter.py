from fastapi import Request, Response
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi import _rate_limit_exceeded_handler

limiter = Limiter(key_func=get_remote_address, default_limits=["5/minute"])

def rate_limit_exceeded_handler(request: Request, exc: Exception) -> Response:
    return _rate_limit_exceeded_handler(request, exc)  # type: ignore
