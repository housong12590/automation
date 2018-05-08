# -*- coding: utf-8 -*-
import getopt
import sys
import os
import re
import json
import requests
import paramiko
import datetime

"""
help == -h 帮助 (未完成)

run 运行容器 ,如果不加此参数 , 只build和push (可选)

-i --image==haiwei/chaos 镜像名称(必须)

-f --dockerfile=docker/Dockerfile  指定dockerfile文件位置, 默认在项目根目录下 (可选)
--tag= 0.1 可以指定构建镜像的tag , 默认为时间格式如:2018092836 (可选)

-n 不发送消息通知 (可选)
--pro=master 暂时用不到(可选)
--dev=develop 暂时用不到(可选)
--token='9d6da20b7e3e596c660b5b6379a2e10f962b823d076c11bbfea3f393bfdcb1cd' 钉钉通知的群组(可选)

#默认部署到192.168.0.212上, 没有别的需要不用填写(可选)

-h 192.168.0.212 项目需要部署的远端地址(可选)
-u root 远端登录的用户名(可选)
-p 123456 远端登录的密码(可选)

cmd和config 只需要一个就可以了,如果两个都添加,优先使用cmd命令(必须)
-c --config 容器运行的docker命令文件 默认为根目录下的run_container.sh
--cmd=docker docker容器运行的命令
"""

image_name = None
dockerfile = '.'

registry = '192.168.0.210'

image_tag = datetime.datetime.now().strftime("%Y%m%d%H%S%M")
clear_image = False
send_message = True

harbor_user = '304536797@qq.com'
harbor_pwd = 'Pss123546'

pro = 'master'
dev = 'develop'
token = '9d6da20b7e3e596c660b5b6379a2e10f962b823d076c11bbfea3f393bfdcb1cd'

ssh_host = None
ssh_user = None
ssh_pwd = None
run_docker_config = 'run_container.sh'
command = None

is_run = False
is_build = False

# 钉钉通知
dd_url = 'https://oapi.dingtalk.com/robot/send?access_token={0}'.format(token)


def parse_args(argv):
    global image_name, dockerfile, image_tag, pro, dev, token, send_message, clear_image, \
        ssh_pwd, ssh_user, ssh_host, run_docker_config, command, is_build, is_run
    short_args = 'nbrf:i:t:h:u:p:c:'
    long_args = ['image=', 'dockerfile=', 'tag=', 'pro=', 'dev=', 'token=', 'host=', 'user=',
                 'password=', 'config=', 'cmd=']
    try:
        opts, args = getopt.getopt(argv, short_args, long_args)
        for o, a in opts:
            if o in ('-i', '--image'):
                image_name = a
            elif o in ('-f', '--dockerfile'):
                dockerfile = a
            elif o in ('-t', '--tag'):
                image_tag = a
            elif o == '--pro':
                pro = a
            elif o == '--dev':
                dev = a
            elif o == '--token':
                token = a
            elif o == '-n':
                send_message = False
            if o in ('-h', '--host'):
                ssh_host = a
            elif o in ('-u', '--user'):
                ssh_user = a
            elif o in ('-p', '--password'):
                ssh_pwd = a
            elif o in ('-c', '--config'):
                run_docker_config = a
            elif o == '--cmd':
                command = a
            elif o == '-b':
                is_build = True
            elif o == '-r':
                is_run = True
        if image_name is None:
            raise Exception('image name is null, use -i or --image==xxx/xxx ...............')
        handle_run_command()
        # 构建并推送镜像
        if is_build:
            build_push_image()
        # 是否需要发送消息通知
        if send_message:
            send_notification()
        # 是否需要运行容器
        if is_run:
            run_container()
    except getopt.GetoptError:
        usage()


def git_branch():
    git_last_log = os.popen('git log -1 --graph --decorate').read()
    branch = re.findall(r'origin/(.*?)\)', git_last_log)
    if len(branch) == 0:
        return None
    else:
        return branch[0]


def send_notification():
    headers = {'content-type': 'application/json;charset=utf-8'}
    content = 'image tag %s run command ->  %s ' % (image_tag, command)
    data = {'msgtype': 'markdown', 'markdown': {'title': '消息通知', 'text': '> \n%s' % content}}
    result = requests.post(dd_url, data=json.dumps(data), headers=headers)
    if result.status_code == 200:
        print(result.text)
        print("发送通知消息成功.......")
    else:
        print("发送通知消息失败.......")


def build_push_image():
    os.system('docker build -t {}/{}:{} {}'.format(registry, image_name, image_tag, dockerfile))
    os.system('docker login {} -u {} -p {}'.format(registry, harbor_user, harbor_pwd))
    os.system('docker tag {0}/{1}:{2} {0}/{1}'.format(registry, image_name, image_tag))
    os.system('docker push {}/{}:{}'.format(registry, image_name, image_tag))
    os.system('docker push {}/{}'.format(registry, image_name))
    os.system('docker rmi {0}/{1}:{2} {0}/{1}'.format(registry, image_name, image_tag))


def run_container():
    if image_name.find('/') != -1:
        container_name = image_name.split('/')[1]
    else:
        container_name = image_name
    global command
    print(command)
    cmds = [
        'docker login {} -u {} -p {}'.format(registry, harbor_user, harbor_pwd),
        'docker rm -f {}'.format(container_name),
        'docker rmi -f {}'.format(image_name),
        'docker pull {}/{}'.format(registry, image_name),
        re.sub(r"\s{2,}", " ", command)
    ]
    if ssh_host is None:
        for cmd in cmds:
            os.system(cmd)
    else:
        ssh_login(cmds)


def ssh_login(cmds):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ssh_host, 22, username=ssh_user, password=ssh_pwd, timeout=20)
    for cmd in cmds:
        stdin, stdout, stderr = client.exec_command(cmd)
        if stderr:
            print(stderr.read())
    client.close()


def format_command(cmd):
    index = cmd.find('docker run')
    cmd = cmd[index:]
    cmd = cmd.replace('\\', '')
    return re.sub(r"\s{2,}", " ", cmd)


def handle_run_command():
    global command
    if command:
        command = format_command(command)
    else:
        if os.path.exists(run_docker_config):
            f = open(run_docker_config, 'r')
            command = format_command(f.read())
            f.close()
        else:
            raise Exception('docker run command is null ,'
                            ' use --cmd or --config=xxx or '
                            'run_container.sh Put it in the project root directory ...........')


def main():
    argv = sys.argv[1:]
    try:
        global is_run
        cmd = argv[0]
        if cmd == '-h' and cmd == 'help':
            usage()
        # elif cmd == 'run':
        #     is_run = True
        #     parse_args(argv[1:])
        else:
            parse_args(argv)
    except IndexError:
        usage()


def usage():
    print('command parameter format error')
    sys.exit(1)


if __name__ == '__main__':
    main()
