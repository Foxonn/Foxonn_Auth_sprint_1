from app.models.jwt_token_models import JWTTokenModels
from app.plugins.auth_plugin.exceptions import FingerprintIsNotValidateError
from app.plugins.auth_plugin.exceptions import TokenNotActiveError
from app.plugins.auth_plugin.impl import Fingerprint
from app.plugins.session_auth_storage_plugin.core import ISessionStorage

__all__ = [
    'AuthSession',
    'AuthSessionFactory',
]


class AuthSession:
    __slots__ = (
        '_fernet',
        '_fingerprint',
        '_session_storage',
        '_jwt_token',
    )

    def __init__(
        self,
        jwt_token: JWTTokenModels,
        session_storage: ISessionStorage,
        fingerprint: Fingerprint,
    ) -> None:
        self._jwt_token = jwt_token
        self._session_storage = session_storage
        self._fingerprint = fingerprint

    @property
    def jwt_token(self) -> JWTTokenModels:
        return self._jwt_token

    async def check_fingerprint(self) -> None:
        fp_from_client = self._jwt_token.payload.fingerprint
        fp_from_storage = self._session_storage.get(self._jwt_token.token).payload.fingerprint

        if fp_from_client != fp_from_storage:
            raise FingerprintIsNotValidateError()

    async def check_token_is_active(self) -> None:
        try:
            self._session_storage.get(token=self._jwt_token.token)
        except KeyError:
            raise TokenNotActiveError()


class AuthSessionFactory:
    __slots__ = (
        '_fingerprint',
        '_session_storage',
    )

    def __init__(
        self,
        fingerprint: Fingerprint,
        session_storage: ISessionStorage,
    ) -> None:
        self._fingerprint = fingerprint
        self._session_storage = session_storage

    async def __call__(
        self,
        jwt_token: JWTTokenModels,
    ) -> AuthSession:
        auth = AuthSession(
            jwt_token=jwt_token,
            session_storage=self._session_storage,
            fingerprint=self._fingerprint,
        )
        await auth.check_token_is_active()
        await auth.check_fingerprint()
        return auth
