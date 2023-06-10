import typing as t

from pony.orm import db_session

from app.functions.query.interfaces import IGetHistoryLogin
from app.plugins.flask_app_plugin.utils.fingerprint import fingerprint_decode
from app.plugins.pony_db_plugin.models import HistoryLogin

__all__ = ['GetHistoryLogin']


class GetHistoryLogin(IGetHistoryLogin):
    __slots__ = ()

    async def __call__(self, user_id: str) -> t.Sequence[t.Mapping[str, t.Any] | None]:
        _ = []
        with db_session:
            for row in HistoryLogin.select(lambda h: str(h.user.id) == user_id).limit(50):
                decode_fingerprint = fingerprint_decode(row.fingerprint)
                _.append({
                    'info': decode_fingerprint,
                    'created_at': row.created_at,
                })
        return _
