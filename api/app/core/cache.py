import json

import redis.asyncio as redis

from app.config import settings

redis_client = redis.from_url(settings.redis_url, decode_responses=True)


async def cache_get(key: str):
    value = await redis_client.get(key)
    return json.loads(value) if value else None


async def cache_set(key: str, value, ttl_seconds: int = 300) -> None:
    await redis_client.set(key, json.dumps(value), ex=ttl_seconds)


async def cache_invalidate(key: str) -> None:
    await redis_client.delete(key)
