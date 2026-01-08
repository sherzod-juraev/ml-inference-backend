from datetime import datetime, timezone
from sqlalchemy import String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as db_uuid, JSON
from uuid import uuid4, UUID
from api.database import Base
from .enums import ModelType, ModelStatus


class MLModel(Base):
    __tablename__ = 'ml_models'

    id: Mapped[UUID] = mapped_column(db_uuid(as_uuid=True), primary_key=True, default=uuid4)
    pipeline: Mapped[dict] = mapped_column(JSON, nullable=False)
    model_type: Mapped[str] = mapped_column(String(250), default=ModelType.single)
    status: Mapped[str] = mapped_column(String(250), default=ModelStatus.ready)
    fit_time: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        index=True
    )

    ml_artifacts: Mapped[list['MLArtifact']] = relationship(
        'MLArtifact',
        foreign_keys='MLArtifact.ml_model_id',
        passive_deletes=True,
        lazy='noload',
        uselist=True
    )


class MLArtifact(Base):
    __tablename__ = 'ml_artifacts'

    id: Mapped[UUID] = mapped_column(db_uuid(as_uuid=True), primary_key=True, default=uuid4)
    ml_model_id: Mapped[UUID] = mapped_column(db_uuid(as_uuid=True), ForeignKey('ml_models.id', ondelete='CASCADE'), nullable=False)
    artifact_type: Mapped[str] = mapped_column(String(250), nullable=False)
    path: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        index=True
    )