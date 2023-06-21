import datetime
import typing as t

from pydantic import BaseModel

__all__ = [
    'JWTTokenModels',
    'JWTAccessTokenModels',
    'JWTRefreshTokenModels',
    'JWTTokenPayloadsModels',
]


class JWTTokenPayloadsModels(BaseModel):
    user_id: str
    fingerprint: str
    exp: datetime.datetime
    roles: t.List[str] | None = None


class JWTTokenModels(BaseModel):
    payload: JWTTokenPayloadsModels
    token: str


class JWTAccessTokenModels(JWTTokenModels):
    pass


class JWTRefreshTokenModels(JWTTokenModels):
    pass
