from docker import config
import re

import sys
import os

git_addr = os.popen('git remote -v')
result = re.findall(r'origin\s+(.*?)\s', git_addr.read())
print(result)
