from pydantic import BaseModel

__all__ = ['LoginEvent']


class LoginEvent(BaseModel):
    login: str
    password: str
    fingerprint: bytes
