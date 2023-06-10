import typing as t
from flask import Response

__all__ = ['make_json_response']


def make_json_response(response: t.Any, status: int) -> Response:
    return Response(response=response, status=status, content_type='text/json')
