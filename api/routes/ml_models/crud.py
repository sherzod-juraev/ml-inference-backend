from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from fastapi import HTTPException, status
from uuid import UUID
from .model import MLModel, MLArtifact
from . import schemas


async def save(
        db: AsyncSession,
        err_text: str,
        /
):
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=err_text
        )


async def create_mlmodel(
        db: AsyncSession,
        mlmodel_schema: schemas.MLModelCreate,
        /
):
    ml_model = MLModel(
        pipeline=mlmodel_schema.pipeline,
        model_type=mlmodel_schema.model_type.value,
        status=mlmodel_schema.status.value,
        fit_time=mlmodel_schema.fit_time
    )
    db.add(ml_model)
    await save(db, 'Error creating ml_model')


async def create_mlartifact(
        db: AsyncSession,
        mlartifact_schema: schemas.MLArtifactCreate,
        /
):
    ml_artifact = MLArtifact(
        ml_model_id=mlartifact_schema.ml_model_id,
        artifact_type=mlartifact_schema.artifact_type,
        path=mlartifact_schema.path
    )
    db.add(ml_artifact)
    await save(db, 'Error creating ml_artifact')


async def read_mlmodel(
        db: AsyncSession,
        mlmodel_id: UUID,
        skip: int,
        limit: int,
        /
) -> MLModel:
    ml_model = await db.get(MLModel, mlmodel_id)
    if ml_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='ML model not found'
        )
    result = await db.execute(
        select(
            MLArtifact).where(
            MLArtifact.ml_model_id==mlmodel_id
        ).order_by(
            MLArtifact.created_at.desc()).offset(
            skip).limit(
            limit)
    )
    ml_model.ml_artifacts = result.scalars().all()
    return ml_model