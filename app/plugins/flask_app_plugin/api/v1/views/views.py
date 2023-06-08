from typing import Any, Mapping

import orjson
from flask import Flask, request, Response
from pony.orm import db_session

from app.exceptions import UserNotFoundError
from app.functions.commands.interfaces import ICreateHistoryLogin, ICreateUser
from app.functions.query.interfaces import IGetHistoryLogin, IIdentificationUser
from app.models import LoginRequestModel, RegistrationRequestModel
from app.plugins.flask_app_plugin.utils import make_json_response
from app.plugins.jwt_token_plugin.functions.commands.interfaces import (
    ICreateAccessTokenCmd,
    ICreateRefreshTokenCmd,
    IDecodeJWTTokenCmd,
)
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
        create_access_token = ioc.get(ICreateAccessTokenCmd)
        create_refresh_token = ioc.get(ICreateRefreshTokenCmd)
        identification_user = ioc.get(IIdentificationUser)
        create_history_login = ioc.get(ICreateHistoryLogin)
        data = LoginRequestModel(**request.args)

        with db_session:
            try:
                user = await identification_user(**data.dict())
                identity = {'user_id': str(user.id)}
            except UserNotFoundError as err:
                return make_json_response(response=str(err), status=404)
            else:
                access_token = create_access_token(payload=identity)
                refresh_token = create_refresh_token(payload=identity)
                # await write_token_to_redis(token)
                await create_history_login(content=request.headers['User-Agent'], user=user)

                return make_json_response(
                    response=orjson.dumps({
                        'access_token': access_token.token,
                        'refresh_token': refresh_token.token,
                    }),
                    status=200,
                )

    @app.route('/refresh', methods=["GET"])
    async def refresh() -> Response:
        create_access_token = ioc.get(ICreateAccessTokenCmd)
        refresh_token = request.args['refresh_token']
        new_token = create_access_token(identity=current_user, fresh=False)
        return make_json_response(
            response=orjson.dumps(new_token),
            status=200,
        )

    @app.route('/logout', methods=["POST"])
    async def logout() -> Mapping[str, Any]:
        ...

    @app.route('/relogin', methods=["POST"])
    async def relogin() -> Mapping[str, Any]:
        ...

    @app.route('/history_login', methods=["GET"])
    async def history_login() -> Response:
        get_history_login = ioc.get(IGetHistoryLogin)
        decode_jwt_token_cmd = ioc.get(IDecodeJWTTokenCmd)

        authorization_token = request.headers.get('Authorization').split()[-1]
        token = decode_jwt_token_cmd(authorization_token)

        result = await get_history_login(user_id=token.payload.user_id)
        try:
            return make_json_response(response=orjson.dumps(result), status=200)
        except BaseException as err:
            return make_json_response(response=orjson.dumps({'error': str(err)}), status=500)
