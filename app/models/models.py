from pydantic import BaseModel

__all__ = [
    'LoginResponseModel',
    'RegistrationRequestModel'
]


class LoginResponseModel(BaseModel):
    access_token: str
    refresh_token: str


class RegistrationRequestModel(BaseModel):
    login: str
    password: str
