from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import APIRouter, Request, Response, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from api.database import get_db
from api.core import security
from config import get_setting
from . import crud, schemas


user_router = APIRouter()
settings = get_setting()


@user_router.post(
    '/sign/up',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Token
)
async def create_user(
        response: Response,
        user_form: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Annotated[AsyncSession, Depends(get_db)]
):
    user_schema = schemas.UserCreate(
        username=user_form.username,
        password=user_form.password
    )
    user_model = await crud.create(db, user_schema)
    response.set_cookie(
        key='refresh_token',
        value=security.create_refresh_token(user_model.id),
        max_age=60 * 60 * 24 * settings.refresh_token_days,
        expires=datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_days),
        httponly=True
    )
    token = schemas.Token(
        access_token=security.create_access_token(user_model.id)
    )
    return token


@user_router.post(
    '/refresh',
    status_code=status.HTTP_200_OK,
    response_model=schemas.Token
)
async def update_token(
        request: Request,
        response: Response
):
    refresh_token = request.cookies.get('refresh_token')
    user_id = security.verify_refresh_token(refresh_token)
    response.set_cookie(
        key='refresh_token',
        value=security.create_refresh_token(user_id),
        max_age=60 * 60 * 24 * settings.refresh_token_days,
        expires=datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_days),
        httponly=True
    )
    token = schemas.Token(
        access_token=security.create_access_token(user_id)
    )
    return token


@user_router.put(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=schemas.UserRead
)
async def full_update(
        user_id: Annotated[UUID, Depends(security.verify_access_token)],
        user_schema: schemas.UserUpdateFull,
        db: Annotated[AsyncSession, Depends(get_db)]
):
    user_model = await crud.update(db, user_id, user_schema)
    return user_model


@user_router.patch(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=schemas.UserRead
)
async def partial_update(
        user_id: Annotated[UUID, Depends(security.verify_access_token)],
        user_schema: schemas.UserUpdatePartial,
        db: Annotated[AsyncSession, Depends(get_db)]
):
    user_model = await crud.update(db, user_id, user_schema, exclude_unset=True)
    return user_model


@user_router.delete(
    '/',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_user(
        response: Response,
        user_id: Annotated[UUID, Depends(security.verify_access_token)],
        db: Annotated[AsyncSession, Depends(get_db)]
):
    await crud.delete(db, user_id)
    response.delete_cookie(key='refresh_token')


@user_router.get(
    '/me',
    status_code=status.HTTP_200_OK,
    response_model=schemas.UserRead
)
async def get_user(
        user_id: Annotated[UUID, Depends(security.verify_access_token)],
        db: Annotated[AsyncSession, Depends(get_db)]
):
    user_model = await crud.read(db, user_id)
    return user_model