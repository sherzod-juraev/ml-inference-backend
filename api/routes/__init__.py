from fastapi import APIRouter

from .users import user_router
from .ml_models import ml_model_router


routes_router = APIRouter()

routes_router.include_router(
    user_router,
    prefix='/auth',
    tags=['Authenticate']
)

routes_router.include_router(
    ml_model_router,
    prefix='/ml_models',
    tags=['ML models']
)