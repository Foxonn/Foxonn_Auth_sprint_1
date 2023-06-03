from typing import Any, Mapping

import orjson
from flask import Flask, make_response, request, Response

from app.functions.commands.interfaces import ICreateUser
from app.models import RegistrationRequestModel
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
    async def login() -> Mapping[str, Any]:
        ...

    @app.route('/logout', methods=["POST"])
    async def logout() -> Mapping[str, Any]:
        ...

    @app.route('/relogin', methods=["POST"])
    async def relogin() -> Mapping[str, Any]:
        ...
