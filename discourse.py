import requests


class DiscourseClient(object):
    def __init__(self, host, api_username, api_key):

        self.host = host
        self.api_username = api_username
        self.api_key = api_key
        self.params = {'api_key': api_key, "api_username": api_username}
        self.headers = {"Accept": "application/json; charset=utf-8"}

    def user(self, username):
        return self._get("/users/{0}.json".format(username))

    def new_post(self, title=None, content="Default Message", id=None):
        post = {}
        if title is not None:
            post.update({"title": title})
        if id is not None:
            post.update({"topic_id": id})
        post.update({"raw": content})
        post.update({"category": 56})

        response = requests.post(
            '{}/posts?api_key={}&api_username={}'.format(self.host, self.api_key, self.api_username),
            data=post, headers={"Content-Type": "application/x-www-form-urlencoded;"})

    def send_pm(self, username=None, title=None, content="Default Message", id=None):
        post = {}
        if title is not None:
            post.update({"title": title})
        if id is not None:
            post.update({"topic_id": id})
        post.update({"raw": content})
        if username is not None:
            post.update({"target_usernames": username})
        post.update({"archetype": "private_message"})

        response = requests.post('{}/posts?api_key={}&api_username={}'.format(self.host, self.api_key, self.api_username),
                                 data=post, headers={"Content-Type": "application/x-www-form-urlencoded;"})

        return response

    def get_likes(self, id):
        return self._get("/post_action_users?id={}&post_action_type_id=2".format(id))

    def get_pms(self, username):
        return self._get("/topics/private-messages/{0}.json".format(username))

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
        response = requests.get('{}{}?api_key={}&api_username={}'.format(self.host, path, self.api_key, self.api_username), headers=self.headers)
        return response.json()
