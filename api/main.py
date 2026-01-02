from fastapi import FastAPI, Depends
from .core import register_exception
from .core.redis import redis, global_rate_limit



app = FastAPI(
    dependencies=[
        Depends(global_rate_limit)
    ]
)

register_exception(app)


@app.on_event('startup')
async def start_up():
    await redis.ping()
    print('Redis connection successfully')


@app.on_event('shutdown')
async def shut_down():
    await redis.close()
    await redis.wait_closed()
    print('Redis closed')