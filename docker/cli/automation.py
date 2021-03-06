# -*- coding: utf-8 -*-
import getopt
import sys
import os
import re
import requests
from docker import config
from .docker_build import build_push
from .docker_run import run
from notifiy import send
import io
import json

help_info = """
help 帮助信息
-i --image 镜像名称 可以不指定(如果没有该选项则去docker run命令里面获取)
-f --dockerfile dockerfile文件所在位置,默认在项目根目录下,可以使用相对路径.或者..的方式
-t --tag 镜像生成的tag 默认为时间格式(20180519015156)

-b --build 构建镜像并上传 ,会生成指定tag和latest的两个镜像,并上传至210 harbor镜像仓库
-r --run 运行容器
构建并运行 (简易使用 -br)

--cmd 运行容器所需的命令 可以设置多个cmd命令,会依次执行 如果只是执行build操作,可以不指定

remote 在远端主机运行容器 中间要借助barbor中间件 ,默认是以本机的方式运行

-h --host 远端主机ip (默认 192.168.0.212)
-u --user 远端主机登录用户名(默认 root)
-p --password 远端服务器登录密码(默认 123456)

-n --notify 通知方式目前有两种通知邮件(mail)和钉钉(ding) 默认为钉钉通知
通知方式://通知的用户
示例: mail://304536797@qq.com,452945447@qq.com 
如果有多个通知用户以逗号分开, 钉钉通知填写token即可

--no-send 不发送通知 如果没有build或者run 也不会发送通知

--outer-net 在外网环境下 pull 或者push 镜像, 默认是使用局域网ip 192.168.0.210, 外网使用registry.jiankanghao.net


运行示例:
automation remote -br --cmd="docker run -d --name coasts -p 8086:5000 192.168.0.210/haiwei/coasts"
"""


def parse_command(argv):
    short_args = 'bri:f:t:h:u:p:n:'
    long_args = ['image=', 'dockerfile=', 'tag=', 'host=', 'user=', 'password=', 'cmd=', 'no-send',
                 'outer-net', 'notify', 'registry_user=', 'registry_pwd=']
    try:
        opts, args = getopt.getopt(argv, short_args, long_args)
        for opt, value in opts:
            if opt in ('-i', '--image'):
                config.PULL_ADDRESS = value
            elif opt in ('-f', '--dockerfile'):
                config.DOCKER_FILE = value
            elif opt in ('-t', '--tag'):
                config.IMAGE_TAG = value
            elif opt in ('-h', '--host'):
                config.RUN_HOST = value
            elif opt in ('-u', '--user'):
                config.RUN_USER = value
            elif opt in ('-p', '--password'):
                config.RUN_PASSWORD = value
            elif opt == '--cmd':
                config.COMMAND = value
            elif opt == '-b':
                config.BUILD = True
            elif opt == '-r':
                config.RUN = True
            elif opt in ('-n', '--notify'):
                config.NOTIFY = value
            elif opt == '--no-send':
                config.ON_SEND = True
            elif opt == '--outer-net':
                config.OUTER_NET = True
            elif opt == '--registry_user':
                config.REGISTRY_USER = value
            elif opt == '--registry_pwd':
                config.REGISTRY_PASSWORD = value
    except getopt.GetoptError:
        usage()
        return False
    return True


def git_branch():
    git_last_log = os.popen('git log -1 --graph --decorate').read()
    branch = re.findall(r'origin/(.*?)\)', git_last_log)
    message = re.findall(r'\s{5}(.*?)\n', git_last_log)
    try:
        return branch[0], message[0]
    except IndexError:
        return None, None


def get_image_name():
    try:
        regexp = r' ([\w|\.]*?/\w+?/[\w\-_]+)'
        result = re.findall(regexp, config.COMMAND)
        result = result[len(result) - 1]
        result = result.split('/')
        image_name = '{}/{}'.format(result[1], result[2])
        return image_name
    except Exception:
        raise ValueError('not find image name usage -i --image --cmd')


def check_params():
    if config.RUN and config.COMMAND is None:
        return False
    if config.PULL_ADDRESS is None:
        config.IMAGE_NAME = get_image_name()
        config.PULL_ADDRESS = '192.168.0.210/' + config.IMAGE_NAME + ':' + config.IMAGE_TAG


def execute(args):
    if parse_command(args) is False:
        raise Exception('parse command error...usage help')
    if check_params() is False:
        raise Exception('required parameter missing...')
    if config.BUILD and build_push() is False:
        raise Exception('docker build fail...')
    if config.RUN and run() is False:
        raise Exception('docker run fail...')


def usage():
    print(help_info)
    sys.exit(1)


def send_message(project, result, msg=None):
    if result:
        result = 'success'
    else:
        result = 'fail'
    if msg is None:
        msg = config.PULL_ADDRESS
    send('构建通知  %s...%s' % (project, result), msg)


def get_port():
    results = re.findall(r'-p.*:(\d+?)\s', config.COMMAND)
    port = None
    if len(results) != 0:
        port = results[0]
    return port


def get_host():
    results = re.findall(r'-p\s+(\d+?):', config.COMMAND)
    if len(results) != 0:
        port = results[0]
        return '{}:{}'.format(config.RUN_HOST, port)
    return None


def get_dockerfile_content():
    file = None
    try:
        path = os.path.abspath(os.path.join(config.DOCKER_FILE, 'Dockerfile'))
        file = io.open(path, 'r', encoding='utf8')
        content = file.read()
    except FileNotFoundError:
        content = ''
    finally:
        if file:
            file.close()
    return content


def code_registry():
    try:
        git_addr = os.popen('git remote -v')
        result = re.findall(r'origin\s+(.*?)\s', git_addr.read())
        return result[0]
    except Exception:
        return None


def push_build_result(image_name, status):
    url = config.SERVER_HOST + 'docker/push'
    space_name = config.IMAGE_NAME.split('/')[0]
    if space_name in config.REGISTRY_SPACE:
        branch, message = git_branch()
        data = {
            'image_name': image_name.split('/')[1],
            'image_tag': config.IMAGE_TAG,
            'git_branch': branch,
            'git_message': message,
            'status': status,
            'command': re.sub(r"\s{2,}", " ", config.COMMAND.replace('\\', '')),
            'host': get_host(),
            'port': get_port(),
            'dockerfile': get_dockerfile_content(),
            'pull_address': config.PULL_ADDRESS,
            'notify': config.NOTIFY,
            'send': not config.NO_SEND,
            'code_registry': code_registry()
        }
        result = requests.post(url, data)
        if result.status_code != 200:
            print('push build result error ' + url)


def main():
    argv = sys.argv[1:]
    if 'help' in argv:
        usage()
    elif 'remote' in argv:
        config.ENABLE_REMOTE = True
        argv.remove('remote')
    status = True

    try:
        execute(argv)
    except Exception as e:
        send_message(config.IMAGE_NAME, False, e.args)
        print(e.args)
        exit(1)

    try:
        if config.NO_SEND is False and (config.BUILD or config.RUN):
            send_message(config.IMAGE_NAME, status)
    except Exception as e:
        print('发送通知消息失败', e.args)

    try:
        if config.NO_SEND is False and config.BUILD:
            push_build_result(config.IMAGE_NAME, status)
    except Exception as e:
        print('请求接口失败')


if __name__ == '__main__':
    main()
