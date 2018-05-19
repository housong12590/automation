from subprocess import Popen, PIPE
import os


def run_command(cmd):
    print(cmd)
    if os.system(cmd) != 0:
        return False
    return True
    # raise Exception(cmd + 'execute fail ......')
    # popen = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    # if popen.wait() != 0:
    #     return False
    # return True
