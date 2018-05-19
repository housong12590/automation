from notifiy.ding import Ding

ding = Ding()
ding.send('ceshi', 'jenkins构建通知', '9d6da20b7e3e596c660b5b6379a2e10f962b823d076c11bbfea3f393bfdcb1cd', image='chaos',
          tag='20180519010754')
