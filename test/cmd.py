import os

result = os.system('docker run -d --name mysql -e MYSQL_ROOT_PASSWORD=123456 mysql:5.7')
print(result)
