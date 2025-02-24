from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["60/minute"],
    headers_enabled=True,
    strategy="moving-window"
)

async def rate_limit_exceeded_handler(request, exc):
    logger.warning(
        "Rate limit exceeded",
        extra={
            "path": request.url.path,
            "method": request.method,
            "client_host": request.client.host if request.client else "unknown"
        }
    )
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many requests"}
    )
