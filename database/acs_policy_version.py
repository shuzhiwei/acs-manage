import web, datetime
import os, sys

env = os.environ
host = env.get('host')
port = int(env.get('port'))
user = env.get('user')
password = env.get('password')
db = env.get('database')

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