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

# 根据id删除rule
def delete_rule_on_id(id):
    db.delete('casbin_rule', where="id=$id", vars=locals())

# 删除rule
def delete_rule(p_type, v0, v1, v2, v3):
    if not v3:
        db.delete('casbin_rule', where="p_type=$p_type and v0=$v0 and v1=$v1 and v2=$v2", vars=locals())
    else:
        db.delete('casbin_rule', where="p_type=$p_type and v0=$v0 and v1=$v1 and v2=$v2 and v3=$v3", vars=locals())

# 插入rule
def insert_rule(*args):
    if len(args) == 4:
        db.insert('casbin_rule', p_type=args[0], v0=args[1], v1=args[2], v2=args[3])
    elif len(args) == 5:
        db.insert('casbin_rule', p_type=args[0], v0=args[1], v1=args[2], v2=args[3], v3=args[4])
   
# 获取指定domain的rules
def get_rules(domain):
    try:
        res = db.select('casbin_rule', where='v1=$domain', vars=locals())
        if len(res) > 1:
            res_list = []
            for i in res:
                res_list.append(i)
            return res_list
        else:
            return res[0]
    except Exception as e:
        print(e)
        return 0

# 获取所有的rules
def get_all_rules():
    try:
        res = db.select('casbin_rule', order='id DESC')
        if len(res) > 1:
            res_list = []
            for i in res:
                res_list.append(i)
            return res_list
        else:
            return res[0]
    except Exception as e:
        print(e)
        return 0

# 分页获取rules

# 更新rule
def update_rule(id, p_type, v0, v1, v2, v3):
    db.update('casbin_rule', where='id=$id', vars=locals(), p_type=p_type, v0=v0, v1=v1, v2=v2, v3=v3)


if __name__ == "__main__":
    update_rule(9, 'g', 'shuzhiwei', 'blog', 'admin_role', '')