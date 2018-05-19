from docker import config
from .ding import Ding
from .mail import Mail

item = {
    'ding': Ding,
    'mail': Mail
}


def send(subject, msg, **kwargs):
    msg_type, users = config.NOTIFY.split('//')
    to = users.split(',')
    if msg_type not in item:
        msg_type = 'ding'
    obj = item.get(msg_type)()
    obj.send(subject, msg, to, **kwargs)
