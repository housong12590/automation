from docker import config
from .command import run_command



def build_push():
    IMAGE = '{}/{}'.format(config.REGISTRY, config.IMAGE_NAME)
    commands = [
        'docker login {} -u {} -p {}'.format(config.REGISTRY, config.REGISTRY_USER, config.REGISTRY_PASSWORD),
        'docker build -t {0}:{1} {2}'.format(IMAGE, config.IMAGE_TAG, config.DOCKER_FILE),
        'docker tag {0}:{1} {0}'.format(IMAGE, config.IMAGE_TAG),
        'docker push {0} {0}:{1}'.format(IMAGE, config.IMAGE_TAG),
        'docker rmi -f {0}:{1} {0}'.format(IMAGE, config.IMAGE_TAG)
    ]
    for cmd in commands:
        if run_command(cmd) is False:
            return False
    return True
