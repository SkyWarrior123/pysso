from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from .config import config


class SSOMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        origin = request.headers.get("origin")
        if origin and origin not in config.allowed_origins:
            raise HTTPException(status_code=403, detail="Orgin not allowed")
        response = await call_next(request)
        return response
    



