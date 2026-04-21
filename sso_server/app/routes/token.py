from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..tokens import verify_code, create_jwt
from ..models import TokenRequest

router = APIRouter()

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    expires_in: int = 3600

@router.post("/exchange", response_model=TokenResponse)
async def exchange_code(request: TokenRequest):
    try:
        payload = verify_code(request.code)
        
        if payload["origin"] != request.origin:
            raise HTTPException(400, "Invalid origin")
        
        jwt_token = create_jwt(payload["user_id"], request.origin)
        return TokenResponse(access_token=jwt_token)
    except Exception:
        raise HTTPException(400, "Invalid or expired code")