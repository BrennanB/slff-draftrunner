import requests


class DiscourseClient(object):
    def __init__(self, host, api_username, api_key):

        self.host = host
        self.api_username = api_username
        self.api_key = api_key

    def user(self, username):
        print("Getting user data")
        return self._get("/users/{0}.json".format(username))

    def send_pm(self, username, title, content):
        print("Sending PM")
        post = {
            "title": title,
            "topic_id": 0,
            "raw": content,
            "category": 0,
            "target_usernames": username,
            "archetype": "private_message"
        }

        r = requests.get(self.host, params={"api_username": self.api_username, "api_key": self.api_key})
        SESSION_COOKIE = r.cookies
        print(SESSION_COOKIE)

        response = requests.post('{}/posts'.format(self.host), data=post, params={"api_username": self.api_username, "api_key": self.api_key}, cookies=SESSION_COOKIE, headers={"Accept": "application/json; charset=utf-8"})
        print(response.status_code)
        print(response.links)

    def _get(self, path):
        response = requests.get('{}{}'.format(self.host, path), auth=(self.api_username, self.api_key))
        print(response.status_code)
        return response.json()
