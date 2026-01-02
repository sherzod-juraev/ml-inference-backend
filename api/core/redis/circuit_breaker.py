from .connection import redis
from fastapi import Request, HTTPException, status
from config import get_setting


setting = get_setting()


async def circuit_breaker(request: Request):
    key = f'{setting.cb_key}:{request.url.path}'
    current = await redis.incr(key)
    if current == 1:
        await redis.expire(setting.cb_key, setting.cb_period)
    elif current > setting.circuit_breaker_limit:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail='Server temporarily blocked due to repeated failures'
        )