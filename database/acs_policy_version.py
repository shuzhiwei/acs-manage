import web, datetime
import configparser
import os, sys

# 解析配置
parent_dir = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
config = configparser.ConfigParser()
full_path = parent_dir + '/../confs/config.ini'
config.read(full_path)
host = config.get('mysql', 'host')
port = config.getint('mysql', 'port')
user = config.get('mysql', 'user')
db = config.get('mysql', 'db')
password = config.get('mysql', 'password')
db = web.database(dbn='mysql',host=host, port=port, user=user, pw=password, db=db)

# 获取版本
def get_version():
    res = db.select('acs_policy_version')
    return res[0].version

# 增加版本
def add_version():
    a = db.query('update acs_policy_version set version=version+1 where id=1')
    return a

if __name__ == '__main__':
    print(get_version())