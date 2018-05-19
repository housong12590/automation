import importlib
from docker import config

item = {
    'ding': 'notifiy.ding.Ding',
    'mail': 'notifiy.mail.Mail'
}


def send(subject, msg, **kwargs):
    msg_type, users = config.NOTIFY.split('//')
    to = users.split(',')
    if msg_type not in item:
        msg_type = 'ding'
    module, cls = item.get(msg_type).rsplit('.', maxsplit=1)
    module = importlib.import_module(module)
    obj = getattr(module, cls)
    obj.send(subject, msg, to, **kwargs)
