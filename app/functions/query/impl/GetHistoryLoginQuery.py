import typing as t

from pony.orm import db_session

from app.functions.query.interfaces import IGetHistoryLoginQuery
from app.plugins.auth_plugin.impl import Fingerprint
from app.plugins.pony_db_plugin.models import HistoryLogin
from app.utils.ioc import ioc

__all__ = ['GetHistoryLoginQuery']

get_fingerprint = ioc.get_object(object_type=Fingerprint)


class GetHistoryLoginQuery(IGetHistoryLoginQuery):
    __slots__ = ()

    async def __call__(self, user_id: str) -> t.Sequence[t.Mapping[str, t.Any] | None]:
        fingerprint = get_fingerprint()
        _ = []
        with db_session:
            for row in HistoryLogin.select(lambda h: str(h.user.id) == user_id).limit(50):
                _.append({
                    'fingerprint': fingerprint.fingerprint_decode(row.fingerprint),
                    'created_at': row.created_at,
                })
        return _
