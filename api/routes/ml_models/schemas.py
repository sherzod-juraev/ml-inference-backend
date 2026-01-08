from pydantic import BaseModel, ConfigDict, field_validator, Field
from fastapi import HTTPException, status
from uuid import UUID
from .enums import ModelType, ModelStatus


class MLModelCreate(BaseModel):
    model_config = ConfigDict(extra='forbid')
    pipeline: dict
    model_type: ModelType
    status: ModelStatus
    fit_time: float


    @field_validator('pipeline')
    def verify_pipeline(cls, v):
        if not v:
            raise ValueError('Pipeline cannot be empty')
        return v


class MLArtifactCreate(BaseModel):
    model_config = ConfigDict(extra='forbid')
    ml_model_id: UUID
    artifact_type: str = Field(max_length=250)
    path: str


class MLArtifactRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    atrifact_type: str
    path: str


class MLModelRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    pipeline: dict
    model_type: str
    status: str
    fit_time: float
    ml_artifacts: list[MLArtifactRead] = []