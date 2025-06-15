from fastapi import Request, Response
from fastapi.middleware.cors import CORSMiddleware as FastAPICORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware for adding security headers to responses.
    """
    def __init__(
        self,
        app: ASGIApp,
        *,
        csp: str = "default-src 'self'",
        permissions_policy: str = "geolocation=(), microphone=()",
        xss_protection: str = "1; mode=block",
        x_content_type_options: str = "nosniff",
        referrer_policy: str = "strict-origin-when-cross-origin",
        feature_policy: str = "geolocation 'none'; microphone 'none'"
    ) -> None:
        super().__init__(app)
        self.csp = csp
        self.permissions_policy = permissions_policy
        self.xss_protection = xss_protection
        self.x_content_type_options = x_content_type_options
        self.referrer_policy = referrer_policy
        self.feature_policy = feature_policy
    
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Add security headers
        response.headers["Content-Security-Policy"] = self.csp
        response.headers["Permissions-Policy"] = self.permissions_policy
        response.headers["X-Content-Type-Options"] = self.x_content_type_options
        response.headers["Referrer-Policy"] = self.referrer_policy
        
        # For older browsers
        response.headers["X-XSS-Protection"] = self.xss_protection
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Permitted-Cross-Domain-Policies"] = "none"
        response.headers["Feature-Policy"] = self.feature_policy
        
        # Remove server header
        if "server" in response.headers:
            del response.headers["server"]
        
        return response

class CORSMiddleware(FastAPICORSMiddleware):
    """
    Extended CORS middleware with additional security features.
    """
    def __init__(
        self,
        app: ASGIApp,
        allow_origins: list = None,
        allow_methods: list = None,
        allow_headers: list = None,
        allow_credentials: bool = True,
        expose_headers: list = None,
        max_age: int = 600,
    ) -> None:
        super().__init__(
            app=app,
            allow_origins=allow_origins or ["*"],
            allow_methods=allow_methods or ["*"],
            allow_headers=allow_headers or ["*"],
            allow_credentials=allow_credentials,
            expose_headers=expose_headers or ["X-Process-Time"],
            max_age=max_age,
        )
    
    async def __call__(self, scope, receive, send):
        # Handle preflight requests
        if scope["type"] == "http" and scope["method"] == "OPTIONS":
            response = Response(
                status_code=200,
                headers={"Access-Control-Allow-Origin": "*"},
            )
            await response(scope, receive, send)
            return
        
        await super().__call__(scope, receive, send)
