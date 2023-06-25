from pony.orm import db_session

from app.functions.commands.interfaces import ICreateHistoryLoginCmd
from app.functions.query.interfaces import IIdentificationUserQuery
from app.models.auth_models import LoginRequestModel
from app.plugins.flask_app_plugin.events.login_event import LoginEvent
from app.utils.event_bus import EventHandler

__all__ = ['CreateHistoryLoginEventHandler']


class CreateHistoryLoginEventHandler(EventHandler[LoginEvent]):
    __slots__ = (
        '_identification_user_query',
        '_create_history_login_cmd',
    )

    def __init__(
        self,
        identification_user_query: IIdentificationUserQuery,
        create_history_login_cmd: ICreateHistoryLoginCmd,
    ) -> None:
        self._identification_user_query = identification_user_query
        self._create_history_login_cmd = create_history_login_cmd

    async def __call__(self, event: LoginEvent) -> None:
        login_request = LoginRequestModel(**event.dict())

        with db_session:
            user = await self._identification_user_query(**login_request.dict())
            await self._create_history_login_cmd(fingerprint=event.fingerprint, user=user)
