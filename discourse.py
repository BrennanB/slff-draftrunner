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
        response = requests.post('{}/posts.json'.format(self.host), json=post, auth=(self.api_username, self.api_key))
        print(response.status_code)
        print(response.content)

    def _get(self, path):
        response = requests.get('{}{}'.format(self.host, path), auth=(self.api_username, self.api_key))
        print(response.status_code)
        return response.json()
