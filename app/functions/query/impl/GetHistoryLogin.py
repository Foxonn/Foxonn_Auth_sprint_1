from typing import Any, Mapping, Sequence

from pony.orm import db_session

from app.functions.query.interfaces import IGetHistoryLogin
from app.plugins.pony_db_plugin.models import HistoryLogin

__all__ = ['GetHistoryLogin']


class GetHistoryLogin(IGetHistoryLogin):
    __slots__ = ()

    async def __call__(self, user_id: str) -> Sequence[Mapping[str, Any] | None]:
        _ = []
        with db_session:
            for row in HistoryLogin.select(lambda h: str(h.user.id) == user_id).limit(50):
                _.append({
                    'user_agent': row.content,
                    'created_at': row.created_at,
                })
        return _
