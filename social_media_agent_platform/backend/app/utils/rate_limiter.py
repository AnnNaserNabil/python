from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.core.config import settings

# Initialize rate limiter
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[settings.RATE_LIMIT]
)

def get_rate_limit_exception_handler():
    """
    Returns a custom exception handler for rate limit exceeded errors.
    """
    async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={
                "detail": f"Rate limit exceeded: {exc.detail}",
                "retry_after": f"{exc.retry_after} seconds"
            }
        )
    return rate_limit_exceeded_handler

def get_rate_limiter():
    """
    Returns the rate limiter instance.
    """
    return limiter

def get_rate_limit_exceeded_handler():
    """
    Returns the default rate limit exceeded handler.
    """
    return _rate_limit_exceeded_handler
