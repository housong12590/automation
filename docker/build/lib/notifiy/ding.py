from .base import Base
import requests
import json
from docker import config

host = 'http://123.207.152.86:8023/'


class Ding(Base):

    def __init__(self):
        self.kwargs = {}
        self.headers = {'content-type': 'application/json;charset=utf-8'}
        self.url = 'https://oapi.dingtalk.com/robot/send?access_token={0}'

    def send(self, subject, msg, tokens, **kwargs):
        self.kwargs = kwargs
        if tokens is None:
            return False

        if not isinstance(tokens, list):
            tokens = [tokens, ]

        msg = json.dumps(self.make_message(subject, msg))
        for token in tokens:
            temp_url = self.url.format(token)
            requests.post(temp_url, data=msg, headers=self.headers)
        return True

    def make_message(self, subject, msg):
        project = config.IMAGE_NAME.split('/')[1]
        msg_url = host + "build/{}/{}".format(project, config.IMAGE_TAG)
        # msg_url = host + "build/index"
        return {
            "msgtype": "link",
            "link": {
                "text": msg,
                "title": subject,
                "picUrl": "",
                "messageUrl": msg_url
            }
        }
