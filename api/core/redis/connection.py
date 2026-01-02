from redis.asyncio import Redis
from config import setting


redis = Redis.from_url(
    url=setting.redis_url,
    encoding='utf-8',
    decode_responses=True
)
