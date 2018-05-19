# -*- coding: utf-8 -*-
import getopt
import sys
import os
import re
from docker import config
from .docker_build import build_push
from .docker_run import run
from notifiy import send

help = """
help 帮助信息
-i --image 镜像名称 可以不指定(如果没有该选项则去docker run命令里面获取)
-f --dockerfile dockerfile文件所在位置,默认在项目根目录下,可以使用相对路径.或者..的方式
-t --tag 镜像生成的tag 默认为时间格式(20180519015156)

-b --build 构建镜像并上传 ,会生成指定tag和latest的两个镜像,并上传至210 harbor镜像仓库
-r --run 运行容器
构建并运行 (简易使用 -br)

--cmd 运行容器所需的命令 可以设置多个cmd命令,会依次执行 如果只是执行build操作,可以不指定

-h --host 项目部署的主机(默认 192.168.0.212)
-u --user 远端主机的登录用户名(默认 root)
-p --password 远端主机的登录密码(默认 123456)

-n --notify 通知方式目前有两种通知邮件(mail)和钉钉(ding) 默认为钉钉通知
通知方式://通知的用户
示例: mail://304536797@qq.com,452945447@qq.com 
如果有多个以逗号分号, 钉钉通知填写token即可

--no-send 不发送通知 如果没有build或者run 也不会发送通知

--outer-net 在外网环境下 pull 或者push 镜像, 默认是使用局域网ip, 外网使用registry.jiankanghao.net
"""


def parse_command(argv):
    short_args = 'bri:f:t:h:u:p:n:'
    long_args = ['image=', 'dockerfile=', 'tag=', 'host=', 'user=', 'password=', 'cmd=', 'no-send', 'outer-net',
                 'notify']
    try:
        opts, args = getopt.getopt(argv, short_args, long_args)
        for opt, value in opts:
            if opt in ('-i', '--image'):
                config.IMAGE_NAME = value
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

    except getopt.GetoptError:
        usage()
        return False
    return True


def git_branch():
    git_last_log = os.popen('git log -1 --graph --decorate').read()
    branch = re.findall(r'origin/(.*?)\)', git_last_log)
    if len(branch) == 0:
        return None
    else:
        return branch[0]


def get_image_name():
    try:
        regexp = r' ([\w|\.]*?/\w+?/\w+)'
        result = re.findall(regexp, config.COMMAND)
        result = result[len(result) - 1]
        return result.split('/', maxsplit=1)[1]
    except Exception:
        raise ValueError('not find image name')


def check_params():
    if config.RUN and config.COMMAND is None:
        return False
    if config.IMAGE_NAME is None:
        config.IMAGE_NAME = get_image_name()


def execute(args):
    if parse_command(args) is False:
        raise Exception('parse command error...')
    if check_params() is False:
        raise Exception('required parameter missing...')
    if config.BUILD and build_push() is False:
        raise Exception('docker build fail...')
    if config.RUN and run() is False:
        raise Exception('docker run fail...')


def main():
    argv = sys.argv[1:]
    if 'help' in argv:
        usage()
    else:
        status = True
        try:
            execute(argv)
        except Exception as e:
            status = False
        if not config.NO_SEND and (config.BUILD or config.RUN):
            send_message(status)
        send_message(status)


def usage():
    print(help)
    sys.exit(1)


def send_message(result):
    if result:
        result = 'success'
    else:
        result = 'fail'
    msg = config.REGISTRY + '/' + config.IMAGE_NAME + ':' + config.IMAGE_TAG
    project = config.IMAGE_NAME.split('/')[1]
    send('构建通知  %s...%s' % (project, result), msg)


if __name__ == '__main__':
    main()
