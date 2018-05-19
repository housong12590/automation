from .base import Base
from smtplib import SMTP_SSL
from docker.config import sender, passwd
from email.mime.text import MIMEText
from email.utils import formataddr


class Mail(Base):

    def __init__(self):
        self.__server = SMTP_SSL("smtp.qq.com", 465)

    def send(self, subject, msg, to, **kwargs):
        if to is None:
            return False

        if not isinstance(to, list):
            to = [to, ]

        msg = MIMEText(msg, 'plain', 'utf-8')
        msg['From'] = formataddr(["南京海维数据服务有限公司", sender])
        msg['To'] = formataddr([','.join(to), ''])
        msg['Subject'] = subject

        try:
            self.__server.login(sender, passwd)
            self.__server.sendmail(sender, to, msg.as_string())
            self.__server.quit()
            return True
        except Exception:
            return False
