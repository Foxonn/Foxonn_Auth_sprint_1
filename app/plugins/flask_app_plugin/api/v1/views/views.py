from typing import Any, Mapping

import orjson
from flask import Flask, request, Response
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from pony.orm import db_session

from app.exceptions import UserNotFoundError
from app.functions.commands.interfaces import ICreateHistoryLogin, ICreateUser
from app.functions.query.interfaces import IGetHistoryLogin, IIdentificationUser
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
                identity = orjson.dumps({'user_id': user.id}).decode(encoding='utf-8')
            except UserNotFoundError as err:
                return make_json_response(response=str(err), status=404)
            else:
                access_token = create_access_token(identity=identity)
                refresh_token = create_refresh_token(identity=identity)
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

    @app.route('/history_login', methods=["GET"])
    @jwt_required()
    async def history_login() -> Response:
        get_history_login = ioc.get(IGetHistoryLogin)
        raw_jwt_identity = get_jwt_identity()
        jwt_identity = orjson.loads(raw_jwt_identity)
        result = await get_history_login(user_id=jwt_identity['user_id'])

        try:
            return make_json_response(response=orjson.dumps(result), status=200)
        except BaseException as err:
            return make_json_response(response=orjson.dumps({'error': str(err)}), status=500)
