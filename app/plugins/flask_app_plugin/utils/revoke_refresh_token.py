from app.plugins.session_auth_storage_plugin.core import IPairsTokenStorage
from app.plugins.session_auth_storage_plugin.core import ISessionStorage
from app.utils.ioc import ioc

get_pairs_token_storage = ioc.get_object(object_type=IPairsTokenStorage)
get_session_storage = ioc.get_object(object_type=ISessionStorage)

__all__ = ['logout_cmd']


def logout_cmd(token: str) -> None:
    pairs_token_storage = get_pairs_token_storage()
    session_storage = get_session_storage()
    access, refresh = pairs_token_storage.get(token)

    pairs_token_storage.revoke_token(refresh)
    session_storage.revoke_token(refresh)
    session_storage.revoke_token(access)
