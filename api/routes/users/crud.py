from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from uuid import UUID
from api.core.security import hash_password
from . import schemas
from .model import User


async def save(
        db: AsyncSession,
        err_name: str,
        /
):
    try:
        await db.commit()
    except IntegrityError as ex:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Error {err_name} user'
        )


async def create(
        db: AsyncSession,
        user_schema: schemas.UserCreate,
        /
) -> User:
    user_model = User(
        username=user_schema.username,
        password=hash_password(user_schema.password)
    )
    db.add(user_model)
    await save(db, 'creating')
    return user_model


async def read(
        db: AsyncSession,
        user_id: UUID,
        /
) -> User:
    user_model = await db.get(User, user_id)
    if user_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    return user_model


async def update(
        db: AsyncSession,
        user_id: UUID,
        user_schema: schemas.UserUpdateFull | schemas.UserUpdatePartial,
        /, *,
        exclude_unset: bool = False
) -> User:
    user_model = await read(db, user_id)
    for field, value in user_schema.model_dump(exclude_unset=exclude_unset).items():
        if field != 'password':
            setattr(user_model, field, value)
        else:
            setattr(user_model, field, hash_password(value))
    await save(db, 'updating')
    return user_model


async def delete(
        db: AsyncSession,
        user_id: UUID,
        /
):
    user_model = await read(db, user_id)
    await db.delete(user_model)
    await save(db, 'deleting')