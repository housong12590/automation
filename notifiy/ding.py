from .base import Base
import requests
import json
from docker import config


class Ding(Base):

    def __init__(self):
        self.kwargs = {}
        self.headers = {'content-type': 'application/json;charset=utf-8'}
        self.url = 'https://oapi.dingtalk.com/robot/send?access_token={0}'

    def send(self, subject, msg, to, **kwargs):
        self.kwargs = kwargs
        if to is None:
            return False
        tokens = to
        if not isinstance(to, list):
            tokens = [to, ]

        msg = json.dumps(self.make_message(subject, msg))
        for token in tokens:
            temp_url = self.url.format(token)
            requests.post(temp_url, data=msg, headers=self.headers)
        return True

    def make_message(self, subject, msg):
        try:
            msg_url = config.SERVER_HOST + "docker/deploy/{}".format(config.IMAGE_NAME.split('/')[1])
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
        except Exception:
            raise ValueError('send message error , not find image name')
