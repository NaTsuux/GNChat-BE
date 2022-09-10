from copy import copy
from datetime import datetime

from sqlalchemy import text

from gnchat.main.blueprint import main_blueprint
from gnchat.orm.main import MessageModel, UserModel
from gnchat.utils import PlusEncryptor, BaseFormatter
from gnchat.utils.gnexcept import GNException
from gnchat.utils.response import CODENAME
from gnchat.utils.uuid_utils import get_uuid
from gnchat.utils.wrapper import req_resp_wrapper


@main_blueprint.route("/pmsg", methods=['POST'])
@req_resp_wrapper(PlusEncryptor, BaseFormatter)
def send_message(raw_data):
    user_uuid = raw_data.get('user_uuid', None)
    is_picture = raw_data.get('is_picture', False)
    content = raw_data.get('content', '')

    if UserModel.get_item(user_uuid=user_uuid) is None:
        raise GNException(CODENAME.MSG_USER_NOT_EXISTS)

    message_uuid = get_uuid()

    MessageModel.insert_item(
        MessageModel(
            message_uuid=message_uuid,
            owner_uuid=user_uuid,
            is_picture=is_picture,
            content=content,
            group_id=0,  # default group
            send_time=datetime.utcnow()
        )
    )
    return {"message_uuid": message_uuid}


@main_blueprint.route("/gmsg", methods=['POST'])
@req_resp_wrapper(PlusEncryptor, BaseFormatter)
def get_message(raw_data: dict) -> list:
    user_uuid = raw_data.get('user_uuid', None)

    if not user_uuid:
        raise GNException(CODENAME.BAD_REQUEST)

    user = UserModel.get_user(user_uuid)
    if user is None:
        raise GNException(CODENAME.MSG_USER_NOT_EXISTS)

    count = raw_data.get('count')
    msg_time = raw_data.get('msg_time')
    message_list = get_new_message(user) if not count else get_history_message(msg_time, count)

    return message_list


def get_new_message(user: UserModel) -> list:
    latest_read = copy(user.latest_read)
    user.update_item(latest_read=datetime.utcnow())

    message_list = MessageModel.query.filter_by(group_id=0).filter(
        latest_read < MessageModel.send_time,
    ).order_by(text("-send_time")).limit(20).all()

    return message_list


def get_history_message(msg_time: float, count: int) -> list:
    if not msg_time:
        raise GNException(CODENAME.MSG_TIME_NOT_SPECIFIED)

    message_list = MessageModel.query.filter_by(group_id=0).filter(
        MessageModel.send_time < datetime.fromtimestamp(msg_time)
    ).order_by(text("-send_time")).limit(count).all()

    return message_list
