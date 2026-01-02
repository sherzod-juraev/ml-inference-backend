from .connection import redis
from fastapi import Request, HTTPException, status
from config import setting


async def get_ip_and_url(request: Request, text: str, /, *, include_urlpath: bool) -> str:
    forwarded = request.headers.get('X-Forwarded-For')
    client_ip = forwarded.split(',')[0] if forwarded else request.client.host
    url_path = request.url.path
    key = f'{text}:{url_path}:{client_ip}' if include_urlpath else f'{text}:{client_ip}'
    return key


async def rate_limit_helper(key: str, rate_limit: int, rate_period: int, /):

    current = await redis.incr(key)
    if current == 1:
        await redis.expire(key, rate_period)
    elif current > rate_limit:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail='Too many requests'
        )


async def global_rate_limit(request: Request):
    key = await get_ip_and_url(request, 'global_limit', include_urlpath=False)
    await rate_limit_helper(key, setting.global_rate_limit, setting.global_rate_period)


async def rate_limit(request: Request):
    key = await get_ip_and_url(request, 'rate_limit', include_urlpath=True)
    await rate_limit_helper(key, setting.rate_limit, setting.rate_period)