import os


class ENVS:
    def __init__(self):
        for item in os.environ:
            if item.startswith("GN"):
                self.__dict__[item] = os.environ.get(item)

    def __getattr__(self, item):
        return self.__dict__.get(item)

    def __setattr__(self, key, value):
        self.__dict__[key] = value
