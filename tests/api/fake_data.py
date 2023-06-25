from pydantic import BaseModel
from pydantic import Field

__all__ = ['fake_user']


class FakeUser(BaseModel):
    login: str = Field(default='fake_user')
    password: str = Field(default='qwerty123')


fake_user = FakeUser()
