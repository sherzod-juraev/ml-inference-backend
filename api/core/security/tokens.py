from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, ExpiredSignatureError
from jose.jwt import encode, decode
from uuid import UUID
from config import get_setting


setting = get_setting()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/sign/up')


def create_access_token(auth_id: UUID, /) -> str:
    data = {
        'sub': str(auth_id),
        'exp': datetime.utcnow() + timedelta(minutes=setting.access_token_minutes)
    }

    access_token = encode(data, setting.secret_key, algorithm=setting.algorithm)
    return access_token


def create_refresh_token(auth_id: UUID, /) -> str:
    data = {
        'sub': str(auth_id),
        'exp': datetime.utcnow() + timedelta(days=setting.refresh_token_days)
    }

    refresh_token = encode(data, setting.secret_key, algorithm=setting.algorithm)
    return refresh_token


def verify_token(token: str | None, token_type: str, /, *, include_header: bool) -> UUID:
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'{token_type} not found'
        )
    try:
        payload = decode(token, setting.secret_key, algorithms=[setting.algorithm])
        auth_id = payload.get('sub')
        if auth_id is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'auth_id not found from {token_type}'
            )
        return UUID(auth_id)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'{token_type} expired',
            headers={
                'WWW-Authenticate': 'Bearer'
            } if include_header else None
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'{token_type} invalid',
            headers={
                'WWW-Authenticate': 'Bearer'
            } if include_header else None
        )


def verify_access_token(access_token: Annotated[str, Depends(oauth2_scheme)], /) -> UUID:
    return verify_token(access_token, 'access_token', include_header=True)


def verify_refresh_token(refresh_token: str | None, /) -> UUID:
    return verify_token(refresh_token, 'refresh_token', include_header=False)