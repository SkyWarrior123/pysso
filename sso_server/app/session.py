import hashlib
import time
from typing import Dict, Optional
import aioredis
from .config import config

class SessionStore:
    def __init__(self):
        self.redis = None
    
    async def init(self):
        self.redis = await aioredis.from_url(config.redis_url)
    
    async def create_session(self, user_id: str) -> str:
        session_id = hashlib.sha256(f"{user_id}:{time.time()}".encode()).hexdigest()
        await self.redis.setex(f"global_session:{session_id}", 3600, user_id)
        return session_id
    
    async def get_session(self, session_id: str) -> Optional[str]:
        user_id = await self.redis.get(f"global_session:{session_id}")
        return user_id.decode() if user_id else None
    
    async def delete_session(self, session_id: str):
        await self.redis.delete(f"global_session:{session_id}")