from fastapi import FastAPI, Depends
from .routes import routes_router
from .core import register_exception
from .core.redis import redis, global_rate_limit



app = FastAPI(
    dependencies=[
        Depends(global_rate_limit)
    ]
)

app.include_router(routes_router)
register_exception(app)


@app.on_event('startup')
async def start_up():
    await redis.ping()


@app.on_event('shutdown')
async def shut_down():
    await redis.close()