import re


def get_image_name():
    try:
        regexp = r' ([\w|\.]*?/\w+?/[\w\-_]+)'
        result = re.findall(regexp, "docker run -d --name haiwei-k8s-pro-log --restart always 192.168.0.210/haiwei/haiwei_k8s-pro-log")
        result = result[len(result) - 1]
        print(result)
        result = result.split('/')
        image_name = '{}/{}'.format(result[1], result[2])
        return image_name
    except Exception:
        raise ValueError('not find image name usage -i --image --cmd')
name = get_image_name()
print(name)