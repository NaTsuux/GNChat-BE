import json


class BaseEncryptor:
    def __init__(self):
        pass

    @staticmethod
    def encrypt(data):
        return data

    @staticmethod
    def decrypt(data):
        return json.loads(data.decode('utf-8'))
