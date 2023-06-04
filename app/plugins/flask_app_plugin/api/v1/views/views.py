from typing import Any, Mapping

import orjson
from flask import Flask, request, Response
from flask_jwt_extended import create_access_token, create_refresh_token
from pony.orm import db_session

from app.exceptions import UserNotFoundError
from app.functions.commands.interfaces import ICreateHistoryLogin, ICreateUser
from app.functions.query.interfaces import IIdentificationUser
from app.models import LoginRequestModel, RegistrationRequestModel
from app.plugins.flask_app_plugin.utils import make_json_response
from app.utils.ioc import ioc

__all__ = [
    'init_views',
]


def init_views(app: Flask) -> None:
    @app.route('/registration', methods=["POST"])
    async def registration() -> Response:
        create_user = ioc.get(ICreateUser)
        data = RegistrationRequestModel(**request.args)
        try:
            await create_user(data=data.dict())
        except BaseException as err:
            return make_json_response(response=orjson.dumps({'error': str(err)}), status=500)
        return make_json_response(response='', status=200)

    @app.route('/login', methods=["POST"])
    async def login() -> Response:
        identification_user = ioc.get(IIdentificationUser)
        create_history_login = ioc.get(ICreateHistoryLogin)
        data = LoginRequestModel(**request.args)

        with db_session:
            try:
                user = await identification_user(**data.dict())
            except UserNotFoundError as err:
                return make_json_response(response=str(err), status=404)
            else:
                access_token = create_access_token(identity=str(user.id))
                refresh_token = create_refresh_token(identity=str(user.id))
                await create_history_login(content=request.headers['User-Agent'], user=user)

                return make_json_response(
                    response=orjson.dumps({
                        'access_token': access_token,
                        'refresh_token': refresh_token,
                    }),
                    status=200,
                )

    @app.route('/logout', methods=["POST"])
    async def logout() -> Mapping[str, Any]:
        ...

    @app.route('/relogin', methods=["POST"])
    async def relogin() -> Mapping[str, Any]:
        ...
