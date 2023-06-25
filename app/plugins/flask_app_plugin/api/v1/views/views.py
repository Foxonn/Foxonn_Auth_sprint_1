import json

import orjson
from logging import Logger
from flask import Flask
from flask import Response
from flask import request
from jwt import ExpiredSignatureError
from pony.orm import db_session

from app.exceptions import UserNotFoundError
from app.functions.commands.interfaces import ICreateUserCmd
from app.functions.query.interfaces import IGetHistoryLoginQuery
from app.functions.query.interfaces import IIdentificationUserQuery
from app.models.auth_models import LoginRequestModel
from app.models.auth_models import RegistrationRequestModel
from app.plugins.auth_plugin.exceptions import TokenExpiredError
from app.plugins.auth_plugin.exceptions import TokenNotActiveError
from app.plugins.auth_plugin.impl import Fingerprint
from app.plugins.auth_plugin.utils.get_token_session import get_auth_session
from app.plugins.flask_app_plugin.events import LoginEvent
from app.plugins.flask_app_plugin.utils.make_json_response import make_json_response
from app.plugins.jwt_token_plugin.functions.commands.interfaces import ICreateAccessTokenCmd
from app.plugins.jwt_token_plugin.functions.commands.interfaces import ICreateRefreshTokenCmd
from app.plugins.jwt_token_plugin.functions.commands.interfaces import IDecodeJWTTokenCmd
from app.plugins.session_auth_storage_plugin.core import ISessionStorage
from app.utils.ioc import ioc
from app.utils.event_bus import event_bus

__all__ = [
    'init_views',
]

get_logger = ioc.get_object(object_type=Logger)
get_fingerprint = ioc.get_object(object_type=Fingerprint)
get_session_storage = ioc.get_object(object_type=ISessionStorage)
identification_user_query = ioc.get_function(function_type=IIdentificationUserQuery)
create_access_token_cmd = ioc.get_function(function_type=ICreateAccessTokenCmd)
create_refresh_token_cmd = ioc.get_function(function_type=ICreateRefreshTokenCmd)
decode_jwt_token_cmd = ioc.get_function(function_type=IDecodeJWTTokenCmd)
get_history_login_query = ioc.get_function(function_type=IGetHistoryLoginQuery)


def init_views(app: Flask) -> Response:
    logger = get_logger()

    @app.route('/registration', methods=["POST"])
    async def registration() -> Response:
        create_user = ioc.get_function(function_type=ICreateUserCmd)
        data = RegistrationRequestModel(**request.json)

        try:
            with db_session:
                await create_user(data=data.dict())
        except BaseException as err:
            logger.exception(msg=str(err), exc_info=False)
            return make_json_response(response=orjson.dumps({'error': str(err)}), status=500)
        return make_json_response(status=201)

    @app.route('/login', methods=["POST"])
    async def login() -> Response:
        fingerprint = get_fingerprint()
        session_storage = get_session_storage()
        fingerprint = fingerprint.fingerprint_encode()

        login_data = LoginRequestModel(**orjson.loads(request.data))

        await event_bus.publish(
            event=LoginEvent(
                login=login_data.login,
                password=login_data.password,
                fingerprint=fingerprint,
            ),
        )
        with db_session:
            try:
                user = await identification_user_query(**login_data.dict())
                identity = {'user_id': str(user.id), 'fingerprint': str(fingerprint)}
            except UserNotFoundError as err:
                logger.warning(msg=str(err), exc_info=False)
                return make_json_response(response=str(err), status=404)
            else:
                refresh_token = create_refresh_token_cmd(payload=identity)
                access_token = create_access_token_cmd(payload=identity)

                session_storage.set(jwt_token=access_token)
                session_storage.set(jwt_token=refresh_token)

                return make_json_response(
                    response=orjson.dumps({
                        'access_token': access_token.token,
                        'refresh_token': refresh_token.token,
                    }),
                    status=200,
                )

    # @app.route('/refresh/<refresh_token>', methods=["GET"])
    # async def refresh(refresh_token: str) -> Response:
    #     return make_json_response(
    #         response=orjson.dumps({
    #             'access_token': access_token.token,
    #             'refresh_token': refresh_token.token,
    #         }),
    #         status=200,
    #     )

    # @app.route('/logout', methods=["GET"])
    # async def logout() -> Response:
    #     try:
    #         token = get_token_session()
    #         logout_cmd(token=token.token)
    #     except BearerTokenNotFoundError as err:
    #         return make_json_response(response=orjson.dumps({'error': str(err)}), status=403)
    #     else:
    #         return make_json_response(status=200)

    @app.route('/history_login', methods=["GET"])
    async def history_login() -> Response:
        try:
            auth_session = await get_auth_session()
            result = await get_history_login_query(user_id=auth_session.jwt_token.payload.user_id)
            return make_json_response(response=orjson.dumps(result), status=200)
        except (
            TokenNotActiveError,
            TokenExpiredError,
            ExpiredSignatureError,
        ) as err:
            logger.warning(msg=str(err), exc_info=False)
            return make_json_response(response=orjson.dumps({'error': str(err)}), status=401)
        # except Exception as err:
        #     return make_json_response(response=orjson.dumps({'error': str(err)}), status=500)
