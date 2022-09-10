from gnchat.orm.main import MessageModel, UserModel


class BaseFormatter:

    @staticmethod
    def format(data):
        if isinstance(data, MessageModel):
            data = data.to_dict()
        elif isinstance(data, list):
            data = [BaseFormatter.format(i) for i in data]
        elif isinstance(data, UserModel):
            data = data.to_dict()
        return data
