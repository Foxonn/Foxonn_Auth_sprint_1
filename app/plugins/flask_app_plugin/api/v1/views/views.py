import typing as t

import orjson
from flask import Flask
from flask import request
from flask import Response
from jwt import ExpiredSignatureError
from pony.orm import db_session

from app.exceptions import UserNotFoundError
from app.functions.commands.interfaces import ICreateHistoryLoginCmd
from app.functions.commands.interfaces import ICreateUserCmd
from app.functions.query.interfaces import IGetHistoryLoginQuery
from app.functions.query.interfaces import IIdentificationUserQuery
from app.models.auth_models import LoginRequestModel
from app.models.auth_models import RegistrationRequestModel
from app.plugins.flask_app_plugin.utils.fingerprint import fingerprint_encode
from app.plugins.flask_app_plugin.utils.get_token_session import get_token_session
from app.plugins.flask_app_plugin.utils.make_json_response import make_json_response
from app.plugins.flask_app_plugin.utils.required_auth import required_auth
from app.plugins.jwt_token_plugin.functions.commands.interfaces import ICreateAccessTokenCmd
from app.plugins.jwt_token_plugin.functions.commands.interfaces import ICreateRefreshTokenCmd
from app.plugins.jwt_token_plugin.functions.commands.interfaces import IDecodeJWTTokenCmd
from app.plugins.session_auth_storage_plugin.core import ISessionStorage
from app.utils.ioc import ioc

__all__ = [
    'init_views',
]


def init_views(app: Flask) -> None:
    session_storage = ioc.get_object(object_type=ISessionStorage)()
    identification_user_query = ioc.get_function(function_type=IIdentificationUserQuery)
    create_access_token_cmd = ioc.get_function(function_type=ICreateAccessTokenCmd)
    create_refresh_token_cmd = ioc.get_function(function_type=ICreateRefreshTokenCmd)
    create_history_login_cmd = ioc.get_function(function_type=ICreateHistoryLoginCmd)
    decode_jwt_token_cmd = ioc.get_function(function_type=IDecodeJWTTokenCmd)
    get_history_login_query = ioc.get_function(function_type=IGetHistoryLoginQuery)

    @app.route('/registration', methods=["POST"])
    async def registration() -> Response:
        create_user = ioc.get(ICreateUserCmd)
        data = RegistrationRequestModel(**request.args)

        try:
            with db_session:
                await create_user(data=data.dict())
        except BaseException as err:
            return make_json_response(response=orjson.dumps({'error': str(err)}), status=500)
        return make_json_response(response='', status=200)

    @app.route('/login', methods=["POST"])
    async def login() -> Response:
        data = LoginRequestModel(**request.args)

        with db_session:
            try:
                user = await identification_user_query(**data.dict())
                identity = {'user_id': str(user.id)}
            except UserNotFoundError as err:
                return make_json_response(response=str(err), status=404)
            else:
                access_token = create_access_token_cmd(payload=identity)
                refresh_token = create_refresh_token_cmd(payload=identity)

                fingerprint = fingerprint_encode()
                await create_history_login_cmd(fingerprint=fingerprint, user=user)
                session_storage.set(jwt_token=access_token)

                return make_json_response(
                    response=orjson.dumps({
                        'access_token': access_token.token,
                        'refresh_token': refresh_token.token,
                    }),
                    status=200,
                )

    @app.route('/refresh/<refresh_token>', methods=["GET"])
    async def refresh(refresh_token: str) -> Response:
        try:
            token = decode_jwt_token_cmd(token=refresh_token)
        except ExpiredSignatureError as err:
            return make_json_response(response=orjson.dumps({'error': f'Refresh token. {err}'}), status=401)
        except Exception as err:
            return make_json_response(response=orjson.dumps({'error': str(err)}), status=500)
        else:
            access_token = create_access_token_cmd(payload=token.payload.dict())
            refresh_token = create_refresh_token_cmd(payload=token.payload.dict())

        return make_json_response(
            response=orjson.dumps({
                'access_token': access_token.token,
                'refresh_token': refresh_token.token,
            }),
            status=200,
        )

    @app.route('/logout', methods=["POST"])
    async def logout() -> t.Mapping[str, t.Any]:
        ...

    @app.route('/history_login', methods=["GET"])
    @required_auth
    async def history_login() -> Response:
        token = get_token_session()
        result = await get_history_login_query(user_id=token.payload.user_id)
        try:
            return make_json_response(response=orjson.dumps(result), status=200)
        except BaseException as err:
            return make_json_response(response=orjson.dumps({'error': str(err)}), status=500)
