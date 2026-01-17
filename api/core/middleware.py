from fastapi import Request
from time import perf_counter
from .logging import get_logger


logger = get_logger('middleware')


async def log_requests(request: Request, call_next):
    start = perf_counter()
    response = await call_next(request)
    duration = perf_counter() - start
    client_ip = request.headers.get('X-Forwarded-For')
    if client_ip is None:
        client_ip = request.client.host
    else:
        client_ip = client_ip.split(',')[0].strip()
    route_path = request.scope.get('route')
    if route_path:
        route_path = getattr(route_path, 'path', request.url.path)
    else:
        route_path = request.client.host
    await logger.info(f"{client_ip} {request.method} {route_path} {response.status_code} {duration:3f}ms")
    return response