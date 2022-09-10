import json

from flask import request

from gnchat.main.blueprint import main_blueprint
from gnchat.orm.main import UserModel
from gnchat.utils import BaseEncryptor, BaseFormatter
from gnchat.utils.gnexcept import GNException
from gnchat.utils.response import CODENAME
from gnchat.utils.uuid_utils import get_uuid
from gnchat.utils.wrapper import req_resp_wrapper


@main_blueprint.route('/register', methods=['POST'])
@req_resp_wrapper(BaseEncryptor, BaseFormatter)
def register_user(raw_data: dict) -> dict:
    username = raw_data.get('username', None)
    password = raw_data.get('password', None)
    if not username or not password:
        raise GNException(CODENAME.BAD_REQUEST)

    res = UserModel.query.filter_by(username=username).first()
    if res is not None:
        raise GNException(CODENAME.USERNAME_EXISTS)

    user_uuid = get_uuid()

    UserModel.insert_item(
        UserModel(
            user_uuid=user_uuid,
            username=username,
            password=password,
        )
    )

    return {"user_uuid": user_uuid}


@main_blueprint.route('/login', methods=['POST'])
@req_resp_wrapper(BaseEncryptor, BaseFormatter)
def login_user(raw_data: dict) -> UserModel:
    username = raw_data.get('username', None)
    password = raw_data.get('password', None)
    if not username:
        raise GNException(CODENAME.BAD_REQUEST)
    res = UserModel.query.filter_by(username=username).first()

    # TODO make a register&login check
    if res is None:
        res = UserModel(
            user_uuid=get_uuid(),
            username=username,
            password="123456",
        )
        UserModel.insert_item(res)
    return res
