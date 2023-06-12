import datetime
import typing as t

from pydantic import BaseModel

__all__ = [
    'JWTTokenModels',
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

    @property
    def is_expired_token(self) -> bool:
        if datetime.datetime.utcnow().timestamp() > self.payload.exp.timestamp():
            return True
        return False
