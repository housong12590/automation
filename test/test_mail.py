from notifiy.mail import Mail

m = Mail()
r = m.send('jenkins 构建通知', "测试通知", ['304536797@qq.com', '452945447@qq.com'])
print(r)
