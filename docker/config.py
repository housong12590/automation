import datetime

sender = '304536797@qq.com'

passwd = 'szwkidhsrznxbjbi'

ENABLE_REMOTE = False

RUN_HOST = '192.168.0.212'

RUN_USER = 'root'

RUN_PASSWORD = '123456'

IMAGE_TAG = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

PULL_ADDRESS = None

DOCKER_FILE = '.'

COMMAND = None

BUILD = False

RUN = False

NOTIFY = 'ding//d5bd95ab90a2febd06dd3ce9ba7b6d18a0c9cd086d344c63fc069f624dd65afc'

NO_SEND = False

OUTER_NET = False

IMAGE_NAME = None

REGISTRY = 'registry.jiankanghao.net' if OUTER_NET else '192.168.0.210'

REGISTRY_USER = ''

REGISTRY_PASSWORD = ''

REGISTRY_SPACE = ['haiwei', 'public']

SERVER_HOST = 'http://proxy.jiankanghao.net:50063/'
# SERVER_HOST = 'http://192.168.0.212:8056/'
