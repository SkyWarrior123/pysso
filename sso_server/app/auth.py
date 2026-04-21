from passlib.context import CryptContext
from typing import Dict

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Demo users - (in production use database)
USERS: Dict[str, Dict] = {
    "test@example.com": {
        "password": pwd_context.hash("password123"),
        "name": "Test User"
    }
}

def authenticate_user(email: str, password: str) -> bool:
    user = USERS.get(email)
    if not user:
        return False
    return pwd_context.verify(password, user["password"])