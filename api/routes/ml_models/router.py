from typing import Annotated
from fastapi import APIRouter, Query, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from api.core.security import verify_access_token
from api.core.redis import rate_limit
from api.database import get_db
from . import crud, schemas


ml_model_router = APIRouter(
    dependencies=[
        Depends(rate_limit),
        Depends(verify_access_token)
    ])


@ml_model_router.get(
    '/{mlmodel_id}',
    status_code=status.HTTP_200_OK
)
async def get_mlmodel(
        mlmodel_id: UUID,
        db: Annotated[AsyncSession, Depends(get_db)],
        skip: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=1, le=50)] = 10
):
    ml_model = await crud.read_mlmodel(db, mlmodel_id, skip, limit)
    return ml_model