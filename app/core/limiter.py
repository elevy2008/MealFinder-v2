from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from fastapi import Request, status
import logging

logger = logging.getLogger(__name__)

def get_ip_and_path(request: Request) -> str:
    """Get both IP and path to rate limit by both"""
    ip = get_remote_address(request)
    return f"{ip}:{request.url.path}"

limiter = Limiter(
    key_func=get_ip_and_path,
    default_limits=["5/minute"],
    headers_enabled=True,
    storage_uri="memory://"
)

async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    logger.warning(
        "Rate limit exceeded",
        extra={
            "path": request.url.path,
            "method": request.method,
            "client_host": request.client.host if request.client else "unknown"
        }
    )
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={"detail": "Too many requests"},
        headers={"Retry-After": "60"}  # Fixed 60 second retry window
    )
