import typing as t

from pydantic import BaseModel

__all__ = [
    'JWTTokenModels',
    'JWTTokenPayloadsModels',
]


class JWTTokenPayloadsModels(BaseModel):
    user_id: str
    expired: int
    roles: t.List[str] | None = None


class JWTTokenModels(BaseModel):
    payload: JWTTokenPayloadsModels
    token: str
