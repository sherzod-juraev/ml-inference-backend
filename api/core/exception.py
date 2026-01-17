from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from sqlalchemy.exc import TimeoutError
from pydantic import ValidationError
from .logging import get_logger


async def get_ip_url(request: Request) -> tuple:

    client_ip = request.headers.get('X-Forwarded-For')
    if client_ip:
        client_ip = client_ip.split(',')[0].strip()
    else:
        client_ip = request.client.host
    route_path = request.scope.get('route')
    if route_path:
        route_path = getattr(route_path, 'path', request.url.path)
    else:
        route_path = request.url.path
    return (client_ip, route_path)


def register_exception(app: FastAPI, /):

    logger = get_logger('exception_handler')
    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(
            request: Request,
            exc: RequestValidationError
    ):
        client_ip, route_path = await get_ip_url(request)
        await logger.warning(
            f"{client_ip} {request.method} {route_path} 400 | RequestValidationError | {exc.errors()}"
        )
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'detail': 'Error in request',
                'body': exc.errors()
            }
        )


    @app.exception_handler(ResponseValidationError)
    async def response_validation_exception_handler(
            request: Request,
            exc: ResponseValidationError
    ):
        client_ip, route_path = await get_ip_url(request)
        await logger.warning(
            f"{client_ip} {request.method} {route_path} 503 | ResponseValidationError | {exc.errors()}"
        )
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                'detail': 'Server response error'
            }
        )


    @app.exception_handler(TimeoutError)
    async def timeout_exception_handler(
            request: Request,
            exc: TimeoutError
    ):
        client_ip, route_path = await get_ip_url(request)
        await logger.warning(
            f"{client_ip} {request.method} {route_path} 503 | TimeOutError | {exc}"
        )
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                'detail': 'There are not enough server resources. Please try again later'
            }
        )


    @app.exception_handler(ValidationError)
    async def validation_exception_handler(
            request: Request,
            exc: ValidationError
    ):
        client_ip, route_path = await get_ip_url(request)
        await logger.warning(
            f"{client_ip} {request.method} {route_path} 400 | ValidationError | {exc.errors()}"
        )
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'detail': 'validation error',
                'body': exc.errors()
            }
        )


    @app.exception_handler(Exception)
    async def global_exception_handler(
            request: Request,
            exc: Exception
    ):
        client_ip, route_path = await get_ip_url(request)
        await logger.error(
            f"{client_ip} {request.method} {route_path} 500 | UnexpectedError | {exc}"
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                'detail': 'Internal server error'
            }
        )