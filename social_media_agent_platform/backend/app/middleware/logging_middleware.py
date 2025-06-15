import time
import logging
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for logging HTTP requests and responses.
    """
    def __init__(
        self,
        app: ASGIApp,
        *,
        logger=logger,
        skip_paths: list = None,
    ) -> None:
        super().__init__(app)
        self.logger = logger
        self.skip_paths = set(skip_paths or [])
        self.skip_paths.update({"/health", "/docs", "/openapi.json", "/redoc"})
    
    async def dispatch(self, request: Request, call_next):
        # Skip logging for certain paths
        if request.url.path in self.skip_paths:
            return await call_next(request)
        
        # Log request
        client_host = request.client.host if request.client else "unknown"
        self.logger.info(
            f"Request: {request.method} {request.url.path} from {client_host} "
            f"params={dict(request.query_params)}"
        )
        
        # Process request
        start_time = time.time()
        response = await self._log_response(call_next, request)
        process_time = (time.time() - start_time) * 1000
        process_time = round(process_time, 2)
        
        # Log response
        self.logger.info(
            f"Response: {request.method} {request.url.path} "
            f"status_code={response.status_code} "
            f"processed_in={process_time}ms"
        )
        
        # Add X-Process-Time header
        response.headers["X-Process-Time"] = f"{process_time}ms"
        
        return response
    
    async def _log_response(self, call_next, request: Request) -> Response:
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            self.logger.exception(
                f"Exception occurred: {str(e)}\n"
                f"Request: {request.method} {request.url.path}"
            )
            raise
