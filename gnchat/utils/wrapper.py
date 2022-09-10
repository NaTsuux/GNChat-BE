from functools import wraps
from typing import Type

from flask import request

from gnchat.utils.encryptor import BaseEncryptor
from gnchat.utils.formatter import BaseFormatter
from gnchat.utils.gnexcept import GNException
from gnchat.utils.response import make_data_response, CODENAME


def req_resp_wrapper(encryptor: Type[BaseEncryptor], formatter: Type[BaseFormatter]):
    """
    A wrapper that format and encrypt the request body and response body.
    request -> encryptor.decrypt() -> func -> formatter.format() -> encryptor.encrypt()
    The formatter and encryptor only apply on the `data` value in the response dict.

    Args:
        encryptor:
        formatter:

    Returns:

    """

    def response_wraps(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                raw_req_data = encryptor.decrypt(request.data)
                raw_resp_data = func(raw_req_data, *args, **kwargs)
                fmt_resp_data = formatter.format(raw_resp_data)
                enc_resp_data = encryptor.encrypt(fmt_resp_data)
                response_data = make_data_response(CODENAME.OK, enc_resp_data)
            except GNException as exc:
                response_data = make_data_response(exc.code, exc.message)

            return response_data

        return wrapper

    return response_wraps
