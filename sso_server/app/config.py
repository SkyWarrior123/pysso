from pydantic_settings import BaseSettings
from typing import List

class Config(BaseSettings):
    secret_key: str
    jwt_algorithm: str = "HS256"
    session_secret: str
    redis_url: str = "redis://localhost:6379"
    allowed_origins: List[str] = ["http://localhost:3020"]
    
    class Config:
        env_file = ".env"

config = Config()