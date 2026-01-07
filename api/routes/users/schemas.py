from pydantic import BaseModel, ConfigDict, Field, field_validator, EmailStr
from fastapi import HTTPException, status
from re import match
from uuid import UUID
from .enum import UserRole

username_pattern = r'^[A-Za-z\d_-]{1,50}$'
password_pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[A-Za-z\d_-]{8,25}$'

def verify_field(
        value_type: str,
        value: str,
        pattern: str,
        /
) -> str:
    if not match(pattern, value):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f'{value_type} invalid'
        )
    return value



class UserCreate(BaseModel):
    model_config = ConfigDict(extra='forbid')
    username: str = Field(max_length=100)
    password: str = Field(min_length=8, max_length=25)


    @field_validator('username')
    def verify_username(cls, value):
        return verify_field('Username', value, username_pattern)


    @field_validator('password')
    def verify_password(cls, value):
        return verify_field('Password', value, password_pattern)


class UserUpdateFull(BaseModel):
    model_config = ConfigDict(extra='forbid')
    username: str = Field(max_length=50)
    password: str = Field(min_length=8, max_length=25)
    email: EmailStr = Field(max_length=250)
    role: UserRole = UserRole.user


    @field_validator('username')
    def verify_username(cls, value):
        return verify_field('Username', value, username_pattern)


    @field_validator('password')
    def verify_password(cls, value):
        return verify_field('Password', value, password_pattern)


class UserUpdatePartial(BaseModel):
    model_config = ConfigDict(extra='forbid')
    username: str | None = Field(None, max_length=50)
    password: str | None = Field(None, min_length=8, max_length=25)
    email: EmailStr | None = Field(None, max_length=250)
    role: UserRole | None = None


    @field_validator('username')
    def verify_username(cls, value):
        if value is None:
            return value
        return verify_field('Username', value, username_pattern)


    @field_validator('password')
    def verify_password(cls, value):
        if value is None:
            return value
        return verify_field('Password', value, password_pattern)

class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    username: str
    email: str | None = None
    role: str


class Token(BaseModel):
    model_config = ConfigDict(extra='forbid')
    access_token: str
    token_type: str = 'bearer'