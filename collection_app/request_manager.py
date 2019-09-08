import requests


class RequestManager:

    __instance = None

    def __init__(self):
        if RequestManager.__instance is None:
            RequestManager.__instance = self

        self.session = requests.Session()

    def make_request(self, *args, **kwargs):
        return self.session.get(*args, **kwargs)
