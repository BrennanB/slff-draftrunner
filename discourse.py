import requests


class DiscourseClient(object):
    def __init__(self, host, api_username, api_key):

        self.host = host
        self.api_username = api_username
        self.api_key = api_key

    def user(self, username):
        return self._get("/users/{0}.json".format(username))

    def send_pm(self, username, title, content):
        post = {
            "title": title,
            "raw": content,
            "target_usernames": username,
            "archetype": "private_message"
        }

        response = requests.post('{}/posts?api_key={}&api_username={}'.format(self.host, self.api_key, self.api_username),
                                 json=post, headers={"Content-Type": "application/x-www-form-urlencoded;"})

        return response

    def read_pm(self, pm_id=None):
        if pm_id is None:
            raise Exception("Must include pm_id.")
        pm_data = self.get_topic(pm_id)
        cleaned_posts = []
        for post in pm_data['post_stream']['posts']:
            del post['avatar_template']
            cleaned_posts.append(post)
        return cleaned_posts

    def get_topic(self, topic_id=None):
        if topic_id is None:
            raise Exception("Must include topic_id.")
        return self._get("/t/{0}.json".format(topic_id))

    def _get(self, path):
        response = requests.get('{}{}?api_key={}&api_username={}'.format(self.host, path, self.api_key, self.api_username))
        return response.json()
