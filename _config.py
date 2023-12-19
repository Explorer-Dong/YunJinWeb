'''
配置文件：(模板文件，自定义)
	1. 数据库配置信息
	2. ...
'''

# 数据库的配置信息
HOSTNAME = '127.0.0.1'      # 数据库 ip 地址
PORT = '3306'               # 数据库端口，默认 3306   
DATABASE = ''               # 数据库名
USERNAME = ''               # 数据库用户名
PASSWORD = ''               # 数据库密码

DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI
