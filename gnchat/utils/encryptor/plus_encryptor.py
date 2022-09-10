import json

from .base_encryptor import BaseEncryptor


class PlusEncryptor(BaseEncryptor):

    @staticmethod
    def decrypt(data):
        data = json.loads(data.decode('utf-8')).get('data')
        res = bytearray()
        res.extend(byte - 1 for byte in data)
        return json.loads(res.decode('utf-8'))

    @staticmethod
    def encrypt(data):
        string = json.dumps(data)
        res = [byte + 1 for byte in bytearray(string, 'utf-8')]
        return res
