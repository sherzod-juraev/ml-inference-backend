from datetime import datetime, timezone
from sqlalchemy import String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as db_uuid
from uuid import uuid4, UUID
from api.database import Base
from .enum import UserRole


class User(Base):
    __tablename__ = 'users'

    id: Mapped[UUID] = mapped_column(db_uuid(as_uuid=True), primary_key=True, default=uuid4)
    username: Mapped[str] = mapped_column(String(50), nullable=False, index=True, unique=True)
    password: Mapped[str] = mapped_column(Text, nullable=False)
    email: Mapped[str | None] = mapped_column(String(250), nullable=True, unique=True, index=True)
    role: Mapped[str] = mapped_column(String(250), default=UserRole.user.value)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))