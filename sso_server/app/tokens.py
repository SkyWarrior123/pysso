from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from typing import Dict, Any
from .config import config

def create_code(user_id: str, origin: str) -> str:
    payload = {
        "user_id": user_id,
        "origin": origin,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
        "type": "authorization_code"
    }
    return jwt.encode(payload, config.secret_key, algorithm=config.jwt_algorithm)

def verify_code(token: str) -> Dict[str, Any]:
    try:
        return jwt.decode(token, config.secret_key, algorithms=[config.jwt_algorithm])
    except JWTError:
        raise ValueError("Invalid or expired code")

def create_jwt(user_id: str, origin: str) -> str:
    payload = {
        "sub": user_id,
        "origin": origin,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),
        "iat": datetime.now(timezone.utc)
    }
    return jwt.encode(payload, config.secret_key, algorithm=config.jwt_algorithm)