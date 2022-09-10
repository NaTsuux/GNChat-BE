import json
from enum import Enum

from flask import Response

CODE_MESSAGE_MAP = {
    "0000": "ok",
    "0001": "bad request",

    "A001": "username already exists",

    "B001": "user not exists",
    "B002": "message time not specified but limit specified"
}


class CODENAME(Enum):
    OK = "0000"
    BAD_REQUEST = "0001"

    USERNAME_EXISTS = "A001"

    MSG_USER_NOT_EXISTS = "B001"
    MSG_TIME_NOT_SPECIFIED = "B002"


def make_data_response(code: CODENAME, data=None):
    response = json.dumps(
        {
            "code": code.value,
            "message": CODE_MESSAGE_MAP.get(code.value),
            "data": data
        }
    )
    return Response(
        status=200,
        response=response
    )
