import requests


class LMStudioAPIWrapper:
    BASE_URL = "http://localhost:1234/v1/"

    def __init__(self):
        pass

    def get_models(self):
        response = requests.get(f"{self.BASE_URL}models")
        response.raise_for_status()
        return response.json()

    def post_chat_completions(self, data):
        response = requests.post(f"{self.BASE_URL}chat/completions", json=data)
        response.raise_for_status()
        return response.json()

    def post_completions(self, data):
        response = requests.post(f"{self.BASE_URL}completions", json=data)
        response.raise_for_status()
        return response.json()
