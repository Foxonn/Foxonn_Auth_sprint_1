from pydantic import BaseModel

__all__ = [
    'LoginResponseModel',
    'RegistrationRequestModel',
    'LoginRequestModel',
]


class LoginResponseModel(BaseModel):
    access_token: str
    refresh_token: str


class RegistrationRequestModel(BaseModel):
    login: str
    password: str


class LoginRequestModel(RegistrationRequestModel):
    login: str
    password: str
