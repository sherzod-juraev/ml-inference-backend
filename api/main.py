from fastapi import FastAPI, Depends
from .routes import routes_router
from .core import register_exception, get_logger, log_requests
from .core.redis import redis as my_redis, global_rate_limit
from redis.exceptions import ConnectionError
from .core.logging import all_logger


app = FastAPI(
    dependencies=[
        Depends(global_rate_limit)
    ]
)

app.include_router(routes_router)
app.middleware('http')(log_requests)
register_exception(app)

logger = get_logger('ml_inference')

@app.on_event('startup')
async def start_up():
    try:
        await logger.info('Server started')
        await my_redis.ping()
        await logger.info('Redis connected')
    except ConnectionError as ex:
        await logger.error(f'Redis disconnected | Server unavailable | {str(ex)}')


@app.on_event('shutdown')
async def shut_down():
    await my_redis.close()
    logger.critical('Redis connection lost | Server shutdown detected')
    for i in all_logger:
        await i.shutdown()