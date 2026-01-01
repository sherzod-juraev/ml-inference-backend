from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from sqlalchemy.exc import TimeoutError


def register_exception(app: FastAPI, /):

    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(
            request: Request,
            exc: RequestValidationError
    ):
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
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                'detail': 'There are not enough server resources. Please try again later'
            }
        )