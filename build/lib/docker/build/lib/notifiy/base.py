class Base(object):
    def send(self, subject, msg, to, **kwargs):
        raise NotImplementedError
