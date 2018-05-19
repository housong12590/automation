import datetime

sender = '304536797@qq.com'

passwd = 'szwkidhsrznxbjbi'

ENABLE_REMOTE = False

# 默认钉钉通知使用的token
DING_TOKEN = '9d6da20b7e3e596c660b5b6379a2e10f962b823d076c11bbfea3f393bfdcb1cd'

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

NOTIFY = 'ding//9d6da20b7e3e596c660b5b6379a2e10f962b823d076c11bbfea3f393bfdcb1cd'

NO_SEND = False

OUTER_NET = False

REGISTRY = 'registry.jiankanghao.net' if OUTER_NET else '192.168.0.210'

REGISTRY_USER = '304536797@qq.com'

REGISTRY_PASSWORD = 'Pss123546'

REGISTRY_SPACE = ['haiwei', 'public']

SERVER_HOST = 'http://123.207.152.86:8023/'
