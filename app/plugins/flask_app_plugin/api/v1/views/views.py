import orjson
from flask import Flask
from flask import request
from flask import Response
from jwt import ExpiredSignatureError
from pony.orm import db_session

from app.exceptions import UserNotFoundError
from app.functions.commands.interfaces import ICreateUserCmd
from app.functions.query.interfaces import IGetHistoryLoginQuery
from app.functions.query.interfaces import IIdentificationUserQuery
from app.models.auth_models import RegistrationRequestModel
from app.plugins.flask_app_plugin.events import LoginEvent
from app.plugins.flask_app_plugin.exceptions import BearerTokenNotFoundError
from app.plugins.flask_app_plugin.exceptions import FingerprintIsNotValidateError
from app.plugins.flask_app_plugin.utils.fingerprint import fingerprint_encode
from app.plugins.flask_app_plugin.utils.get_token_session import get_token_session
from app.plugins.flask_app_plugin.utils.make_json_response import make_json_response
from app.plugins.flask_app_plugin.utils.required_auth import required_auth_decorator
from app.plugins.flask_app_plugin.utils.required_auth import validation_fingerprint_decorator
from app.plugins.flask_app_plugin.utils.required_auth import validation_token_and_fingerprint
from app.plugins.flask_app_plugin.utils.revoke_refresh_token import logout_cmd
from app.plugins.jwt_token_plugin.functions.commands.interfaces import ICreateAccessTokenCmd
from app.plugins.jwt_token_plugin.functions.commands.interfaces import ICreateRefreshTokenCmd
from app.plugins.jwt_token_plugin.functions.commands.interfaces import IDecodeJWTTokenCmd
from app.plugins.session_auth_storage_plugin.core import IPairsTokenStorage
from app.plugins.session_auth_storage_plugin.core import ISessionStorage
from app.utils.ioc import ioc
from app.utils.message_bus import message_bus

__all__ = [
    'init_views',
]

get_session_storage = ioc.get_object(object_type=ISessionStorage)
get_pairs_token_storage = ioc.get_object(object_type=IPairsTokenStorage)
identification_user_query = ioc.get_function(function_type=IIdentificationUserQuery)
create_access_token_cmd = ioc.get_function(function_type=ICreateAccessTokenCmd)
create_refresh_token_cmd = ioc.get_function(function_type=ICreateRefreshTokenCmd)
decode_jwt_token_cmd = ioc.get_function(function_type=IDecodeJWTTokenCmd)
get_history_login_query = ioc.get_function(function_type=IGetHistoryLoginQuery)


def init_views(app: Flask) -> Response:
    @app.route('/registration', methods=["POST"])
    async def registration() -> Response:
        create_user = ioc.get_function(function_type=ICreateUserCmd)
        data = RegistrationRequestModel(**request.args)

        try:
            with db_session:
                await create_user(data=data.dict())
        except BaseException as err:
            return make_json_response(response=orjson.dumps({'error': str(err)}), status=500)
        return make_json_response(status=201)

    @app.route('/login', methods=["POST"])
    async def login() -> Response:
        session_storage = get_session_storage()
        pairs_token_storage = get_pairs_token_storage()
        fingerprint = fingerprint_encode()

        await message_bus.publish(
            event=LoginEvent(
                login=request.args['login'],
                password=request.args['password'],
                fingerprint=fingerprint,
            ),
        )
        with db_session:
            try:
                user = await identification_user_query(**dict(request.args))
                identity = {'user_id': str(user.id), 'fingerprint': str(fingerprint)}
            except UserNotFoundError as err:
                return make_json_response(response=str(err), status=404)
            else:
                refresh_token = create_refresh_token_cmd(payload=identity)
                access_token = create_access_token_cmd(payload=identity)

                session_storage.set(jwt_token=access_token)
                session_storage.set(jwt_token=refresh_token)
                pairs_token_storage.set(access_token=access_token, refresh_token=refresh_token)

                return make_json_response(
                    response=orjson.dumps({
                        'access_token': access_token.token,
                        'refresh_token': refresh_token.token,
                    }),
                    status=200,
                )

    @app.route('/refresh/<refresh_token>', methods=["GET"])
    async def refresh(refresh_token: str) -> Response:
        return make_json_response(
            response=orjson.dumps({
                'access_token': access_token.token,
                'refresh_token': refresh_token.token,
            }),
            status=200,
        )

    @app.route('/logout', methods=["GET"])
    async def logout() -> Response:
        try:
            token = get_token_session()
            logout_cmd(token=token.token)
        except BearerTokenNotFoundError as err:
            return make_json_response(response=orjson.dumps({'error': str(err)}), status=403)
        else:
            return make_json_response(status=200)

    @app.route('/history_login', methods=["GET"])
    async def history_login() -> Response:
        try:
            token = get_token_session()
            result = await get_history_login_query(user_id=token.payload.user_id)
            return make_json_response(response=orjson.dumps(result), status=200)
        except BaseException as err:
            return make_json_response(response=orjson.dumps({'error': str(err)}), status=500)
