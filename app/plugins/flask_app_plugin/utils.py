from typing import Any

from flask import Response

__all__ = ['make_json_response']


def make_json_response(response: Any, status: int) -> Response:
    return Response(response=response, status=status, content_type='text/json')
