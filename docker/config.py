import datetime

sender = '304536797@qq.com'

passwd = 'szwkidhsrznxbjbi'

ENABLE_REMOTE = False

RUN_HOST = '192.168.0.212'

RUN_USER = 'root'

RUN_PASSWORD = '123456'

IMAGE_TAG = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

IMAGE_NAME = None

DOCKER_FILE = '.'

COMMAND = None

BUILD = False

RUN = False

NOTIFY = 'ding//d5bd95ab90a2febd06dd3ce9ba7b6d18a0c9cd086d344c63fc069f624dd65afc'

NO_SEND = False

OUTER_NET = False

PROJECT = None

REGISTRY = 'registry.jiankanghao.net' if OUTER_NET else '192.168.0.210'

REGISTRY_USER = '304536797@qq.com'

REGISTRY_PASSWORD = 'Pss123546'

REGISTRY_SPACE = ['haiwei', 'public']

# SERVER_HOST = 'http://123.207.152.86:8023/'
SERVER_HOST = 'http://192.168.0.212:8056/'
