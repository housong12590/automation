from docker import config
import paramiko
import re
from .command import run_command


def _ssh_login(commands):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(config.RUN_HOST, 22, username=config.RUN_USER, password=config.RUN_PASSWORD, timeout=20)
    index = 0
    for cmd in commands:
        print(cmd)
        stdin, stdout, stderr = client.exec_command(cmd)
        print(stdout.read().decode())
        if index == 5 and not re.match(r'\w+', stdout.read().decode()):
            print(stderr.read().decode())
            return False
        index = index + 1
    client.close()
    return True


def run():
    IMAGE = '{}/{}'.format(config.REGISTRY, config.IMAGE_NAME)
    container_name = config.IMAGE_NAME.split('/')[1]
    commands = [
        'docker login {} -u {} -p {}'.format(config.REGISTRY, config.REGISTRY_USER, config.REGISTRY_PASSWORD),
        'docker tag {0} {0}:old'.format(IMAGE),
        'docker rmi -f {}'.format(IMAGE),
        'docker pull {}'.format(IMAGE),
        'docker rm -f {}'.format(container_name),
        re.sub(r"\s{2,}", " ", config.COMMAND.replace('\\', '')),
        'docker rmi -f {}:old'.format(IMAGE)
    ]
    index = 0
    if config.ENABLE_REMOTE:
        return _ssh_login(commands)
    else:
        for cmd in commands:
            print(cmd)
            result = run_command(cmd)
            if index == 5 and result is False:
                return False
            index = index + 1
        return True
