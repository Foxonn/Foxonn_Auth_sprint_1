import typing as t

import orjson
from flask import Flask
from flask import request
from flask import Response
from jwt import ExpiredSignatureError
from pony.orm import db_session

from app.exceptions import UserNotFoundError
from app.functions.commands.interfaces import ICreateHistoryLogin
from app.functions.commands.interfaces import ICreateUser
from app.functions.query.interfaces import IGetHistoryLogin
from app.functions.query.interfaces import IIdentificationUser
from app.models.auth_models import LoginRequestModel
from app.models.auth_models import RegistrationRequestModel
from app.plugins.flask_app_plugin.utils.fingerprint import fingerprint_encode
from app.plugins.flask_app_plugin.utils.identity_session import identity_session
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

create_access_token = ioc.get(ICreateAccessTokenCmd)
create_refresh_token = ioc.get(ICreateRefreshTokenCmd)
identification_user = ioc.get(IIdentificationUser)
create_history_login = ioc.get(ICreateHistoryLogin)
session_storage = ioc.get(ISessionStorage)
decode_jwt_token_cmd = ioc.get(IDecodeJWTTokenCmd)
get_history_login = ioc.get(IGetHistoryLogin)


def init_views(app: Flask) -> None:
    @app.route('/registration', methods=["POST"])
    async def registration() -> Response:
        create_user = ioc.get(ICreateUser)
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
                user = await identification_user(**data.dict())
                identity = {'user_id': str(user.id)}
            except UserNotFoundError as err:
                return make_json_response(response=str(err), status=404)
            else:
                access_token = create_access_token(payload=identity)
                refresh_token = create_refresh_token(payload=identity)
                fingerprint = fingerprint_encode()

                session_storage.set(jwt_token=access_token)

                await create_history_login(fingerprint=fingerprint, user=user)
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
            token = decode_jwt_token_cmd(refresh_token)
        except ExpiredSignatureError as err:
            return make_json_response(response=orjson.dumps({'error': f'Refresh token. {err}'}), status=401)
        except Exception as err:
            return make_json_response(response=orjson.dumps({'error': str(err)}), status=500)
        else:
            access_token = create_access_token(payload=token.payload.dict())
            refresh_token = create_refresh_token(payload=token.payload.dict())

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
        token = identity_session()
        result = await get_history_login(user_id=token.payload.user_id)
        try:
            return make_json_response(response=orjson.dumps(result), status=200)
        except BaseException as err:
            return make_json_response(response=orjson.dumps({'error': str(err)}), status=500)
