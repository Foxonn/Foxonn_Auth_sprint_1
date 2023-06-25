import asyncio
import json
import logging
from json import JSONEncoder
from typing import Any

import orjson
import pytest
from aiohttp import ClientSession

from app.models.auth_models import LoginResponseModel
from tests.api.fake_data import fake_user


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(scope="session")
async def session_with_authorize(session: ClientSession) -> ClientSession:
    async with session.post(url='/login', data=orjson.dumps(fake_user.dict()), raise_for_status=True, timeout=5) as response:
        response_data = await response.text()
        json_data = orjson.loads(response_data)

    authorize_credential = LoginResponseModel(**json_data)

    session = ClientSession(
        base_url='http://localhost:8080',
        headers={'Authorization': f'Bearer {authorize_credential.access_token}'},
    )
    yield session
    await session.close()


@pytest.fixture(scope='session')
async def session() -> ClientSession:
    session = ClientSession(
        base_url='http://localhost:8080',
    )
    yield session
    await session.close()


async def logger() -> logging.Logger:
    logger = logging.Logger(name='api_test')
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
    )
    return logger
