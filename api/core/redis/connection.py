import aioredis
from config import setting


redis = aioredis.from_url(
    url=setting.aioredis_url,
    encoding='utf-8',
    decode_responses=True
)
