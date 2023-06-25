import typing as t

import orjson
from aiohttp import ClientSession

from tests.api.fake_data import fake_user


async def test_registration(
    session: ClientSession,
) -> t.NoReturn:
    async with session.post(url='/registration', data=orjson.dumps(fake_user.dict()), raise_for_status=True, timeout=3) as response:
        assert response.status == 201


async def test_login(
    session: ClientSession,
) -> t.NoReturn:
    async with session.post(url='/login', data=orjson.dumps(fake_user.dict()), raise_for_status=True, timeout=5) as response:
        assert response.status == 200


async def test_history_login(
    session_with_authorize: ClientSession,
) -> t.NoReturn:
    async with session_with_authorize.get(url='/history_login', raise_for_status=True, timeout=5) as response:
        assert response.status == 200
        response_data = await response.text()

    history_logs = orjson.loads(response_data)

    assert history_logs[0]
    assert history_logs[0]['created_at']
    assert history_logs[0]['fingerprint']
