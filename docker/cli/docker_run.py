from docker import config
import paramiko
import re
from .command import run_command


def _ssh_login(commands):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(config.RUN_HOST, 22, username=config.RUN_USER, password=config.RUN_PASSWORD,
                   timeout=20)
    run_status = True
    for cmd in commands:
        print(cmd)
        stdin, stdout, stderr = client.exec_command(cmd)
        stdout = stdout.read().decode()
        print(stdout)
        run_status = is_run_status(cmd, stdout)
        stderr = stderr.read().decode()
        print(stderr)
    client.close()
    return run_status


def run():
    IMAGE = '{}/{}'.format(config.REGISTRY, config.IMAGE_NAME)
    container_name = config.IMAGE_NAME.split('/')[1]
    commands = [
        'docker login {} -u {} -p {}'.format(config.REGISTRY, config.REGISTRY_USER,
                                             config.REGISTRY_PASSWORD),
        'docker tag {0} {0}:old'.format(IMAGE),
        'docker rmi -f {}'.format(IMAGE),
        'docker pull {}'.format(IMAGE),
        'docker rm -f {}'.format(container_name),
        re.sub(r"\s{2,}", " ", config.COMMAND.replace('\\', '')),
        'docker rmi -f {}:old'.format(IMAGE)
    ]
    if config.ENABLE_REMOTE:
        return _ssh_login(commands)
    else:
        run_status = True
        for cmd in commands:
            print(cmd)
            result = run_command(cmd)
            run_status = is_run_status(cmd, result)
        return run_status


def is_run_status(cmd, stdout):
    run_status = True
    if re.match(r'^\s*docker run ', cmd):
        if re.match(r'^\w{64}', stdout):
            run_status = True
        else:
            run_status = False
    return run_status
