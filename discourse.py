import requests

class DiscourseClient(object):

    def __init__(self, host, api_username, api_key):

        self.host = host
        self.api_username = api_username
        self.api_key = api_key

    def user(self, username):
        return self._get("/users/{0}.json".format(username))

    def _get(self, path):
        response = requests.get('{}{}'.format(self.host, path))
        return response.json()
