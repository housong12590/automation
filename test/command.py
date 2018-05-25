from docker import config
import re

print(not config.NO_SEND)

command = """
docker run -d --name coasts --restart always \
-e MODE=dev \
-e SECRET_KEY='ccEQCOnFB1DUE8dDHwMOqZuO9mycYQUtfikG87TloLWUXDnKSyJ5DRxIgTTdi8eX' \
-e MYSQL_HOST='192.168.0.210' \
-e MYSQL_PORT=3306 \
-e MYSQL_USER=root \
-e MYSQL_PASSWORD='hJYC8PsOsUR45wnDQtGle8cqCFbmN9eY' \
-e MYSQL_DB='coasts_development' \
-e REDIS_HOST='192.168.0.210' \
-e REDIS_PORT=6379 \
-e REDIS_PASSWORD='' \
-e REDIS_DB=4 \
-e SMS_HOST='http://192.168.0.212:8011/' \
-e EMAIL_HOST='http://192.168.0.212:8012/' \
-e SENTRY_DSN='http://06869120cbe54e24ad83e893048fed7a:3cbdff17574a474bb37521b2a3fd646d@error.jiankanghao.net/13' \
-p 9898:5000 192.168.0.210/haiwei/coasts
"""
results = re.findall(r'-p\s+(\d+?):', command)

print(config.RUN_HOST + ":" + results[0])
