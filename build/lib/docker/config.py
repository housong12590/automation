import datetime

sender = '304536797@qq.com'

passwd = 'szwkidhsrznxbjbi'

# 默认钉钉通知使用的token
DING_TOKEN = '9d6da20b7e3e596c660b5b6379a2e10f962b823d076c11bbfea3f393bfdcb1cd'

RUN_HOST = '192.168.0.212'

RUN_USER = 'root'

RUN_PASSWORD = '123456'

IMAGE_TAG = datetime.datetime.now().strftime("%Y%m%d%H%S%M")

IMAGE_NAME = 'haiwei/coasts'

DOCKER_FILE = '.'

# COMMAND = None
COMMAND = 'docker run -d --name coasts -p 3306:3306 192.168.0.210/haiwei/coasts:2018'

BUILD = False

RUN = False

NOTIFY = 'ding//9d6da20b7e3e596c660b5b6379a2e10f962b823d076c11bbfea3f393bfdcb1cd'

NO_SEND = False

OUTER_NET = False

REGISTRY = 'registry.jiankanghao.net' if OUTER_NET else '192.168.0.210'

REGISTRY_USER = '304536797@qq.com'

REGISTRY_PASSWORD = 'Pss123546'
