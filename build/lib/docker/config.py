import datetime

sender = '304536797@qq.com'

passwd = 'szwkidhsrznxbjbi'

ENABLE_REMOTE = False

RUN_HOST = '192.168.0.212'

RUN_USER = 'root'

RUN_PASSWORD = '123456'

IMAGE_TAG = datetime.datetime.now().strftime("%Y%m%d%H%S%M")

IMAGE_NAME = None

DOCKER_FILE = '.'

COMMAND = None
# COMMAND = 'docker run -d --name test -p 9096:5000 registry.jiankanghao.net/public/test'

BUILD = False

RUN = False

NOTIFY = 'ding//b6daac8619cc68b20b24d0c7f81ee3f57af5f6fc3f11b6be204cf06d9f829a6b'

NO_SEND = False

OUTER_NET = False

REGISTRY = 'registry.jiankanghao.net' if OUTER_NET else '192.168.0.210'

REGISTRY_USER = '304536797@qq.com'

REGISTRY_PASSWORD = 'Pss123546'

REGISTRY_SPACE = ['haiwei', 'public']

SERVER_HOST = 'http://123.207.152.86:8023/'
