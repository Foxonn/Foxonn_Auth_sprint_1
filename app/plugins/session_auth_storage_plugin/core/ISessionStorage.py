from app.models.jwt_token_models import JWTTokenModels

__all__ = ['ISessionStorage']


class ISessionStorage:
    __slots__ = ()

    def set(self, jwt_token: JWTTokenModels) -> None:
        raise NotImplementedError()

    def get(self, token: str) -> JWTTokenModels:
        raise NotImplementedError()

    def is_active_token(self, token: str) -> bool:
        raise NotImplementedError()

    def revoke_token(self, token: str) -> None:
        raise NotImplementedError()
