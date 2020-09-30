import os, configparser
import web, json
import jwt, time
import threading
import traceback
import casbin
from tools.sync_policy import syncPolicy
from database import casbin_rule, acs_policy_version
from logger.logger import logger

urls = (
    '/policy/update', 'UpdatePolicy',
    '/policy/show', 'ShowPolicy',
    '/policy/add', 'AddPolicy',
    '/policy/delete', 'DeletePolicy',
)

app = web.application(urls, globals())
lock = threading.RLock()

parent_dir = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
config = configparser.ConfigParser()
full_path = parent_dir + '/confs/config.ini'
config.read(full_path)
dom = config.get('acs', 'domain')
# dom = 'acs'
obj = 'config'

class UpdatePolicy:
    def POST(self):
        try:
            web.header("Access-Control-Allow-Origin", "*")
            token = web.input().token
            try:
                parse_token = jwt.decode(token, 'secret', algorithms='HS256')
            except Exception as e:
                logger.error(e)
                logger.error(traceback.format_exc())
                return json.dumps({'status': 'fail', 'code': 402, 'message': 'token expired'})

            id = web.input().id
            p_type = web.input().p_type
            v0 = web.input().v0
            v1 = web.input().v1
            v2 = web.input().v2
            v3 = web.input().v3

            username = parse_token['username']
            e = casbin.Enforcer("confs/model.conf", "confs/policy.csv")
            sub = username
            act = 'read'
            if e.enforce(sub, dom, obj, act):
                rules = casbin_rule.update_rule(id, p_type, v0, v1, v2, v3)
                return json.dumps({'status': 'ok', "code": 200, 'message': 'success', 'data': rules})
            else:
                return json.dumps({'status': 'fail', 'code': 401, 'message': 'unauthorization operation'})
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
            return json.dumps({'status': 'fail', 'code': 500, 'message': str(e)})

class ShowPolicy:
    def GET(self):
        try:
            rules = casbin_rule.get_all_rules()
            return json.dumps({'status': 'ok', "code": 200, 'message': 'success', 'data': rules})
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
            return json.dumps({'status': 'fail', 'code': 500, 'message': str(e)})

    def POST(self):
        try:
            web.header("Access-Control-Allow-Origin", "*")
            token = web.input().token
            try:
                parse_token = jwt.decode(token, 'secret', algorithms='HS256')
            except Exception as e:
                logger.error(e)
                logger.error(traceback.format_exc())
                return json.dumps({'status': 'fail', 'code': 402, 'message': 'token expired'})

            username = parse_token['username']
            e = casbin.Enforcer("confs/model.conf", "confs/policy.csv")
            sub = username
            act = 'read'
            if e.enforce(sub, dom, obj, act):
                rules = casbin_rule.get_all_rules()
                return json.dumps({'status': 'ok', "code": 200, 'message': 'success', 'data': rules})
            else:
                return json.dumps({'status': 'fail', 'code': 401, 'message': 'unauthorization operation'})
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
            return json.dumps({'status': 'fail', 'code': 500, 'message': str(e)})
 
class AddPolicy:
    def GET(self):
        try:
            p_type = web.input().p_type
            v0 = web.input().v0
            v1 = web.input().v1
            v2 = web.input().v2
            v3 = web.input().v3
            if v3:
                casbin_rule.insert_rule(p_type, v0, v1, v2, v3)
                acs_policy_version.add_version()
            else:
                casbin_rule.insert_rule(p_type, v0, v1, v2)
                acs_policy_version.add_version()
            return json.dumps({'status': 'ok', "code": 200})
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
            return json.dumps({'status': 'fail', 'code': 500, 'message': str(e)})

    def POST(self):
        try:
            web.header("Access-Control-Allow-Origin", "*")
            token = web.input().token
            p_type = web.input().p_type
            v0 = web.input().v0
            v1 = web.input().v1
            v2 = web.input().v2
            v3 = web.input().v3
            try:
                parse_token = jwt.decode(token, 'secret', algorithms='HS256')
            except Exception as e:
                logger.error(e)
                logger.error(traceback.format_exc())
                return json.dumps({'status': 'fail', 'code': 402, 'message': 'token expired'})

            username = parse_token['username']
            e = casbin.Enforcer("confs/model.conf", "confs/policy.csv")
            sub = username
            act = 'write'
            if e.enforce(sub, dom, obj, act):
                if v3:
                    casbin_rule.insert_rule(p_type, v0, v1, v2, v3)
                    acs_policy_version.add_version()
                else:
                    casbin_rule.insert_rule(p_type, v0, v1, v2)
                    acs_policy_version.add_version()
                return json.dumps({'status': 'ok', "code": 200, 'message': 'success'})
            else:
                return json.dumps({'status': 'fail', 'code': 401, 'message': 'unauthorization operation'})
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
            return json.dumps({'status': 'fail', 'code': 500, 'message': str(e)})

class DeletePolicy:
    def GET(self):
        try:
            p_type = web.input().p_type
            v0 = web.input().v0
            v1 = web.input().v1
            v2 = web.input().v2
            v3 = web.input().v3
            casbin_rule.delete_rule(p_type, v0, v1, v2, v3)
            acs_policy_version.add_version()
            return json.dumps({'status': 'ok', "code": 200})
        except Exception as e:
            return json.dumps({'status': 'fail', 'code': 500, 'message': str(e)})

    def POST(self):
        try:
            web.header("Access-Control-Allow-Origin", "*")
            token = web.input().token
            ids = web.input().ids
            try:
                parse_token = jwt.decode(token, 'secret', algorithms='HS256')
            except Exception as e:
                logger.error(e)
                logger.error(traceback.format_exc())
                return json.dumps({'status': 'fail', 'code': 402, 'message': 'token expired'})

            username = parse_token['username']
            e = casbin.Enforcer("confs/model.conf", "confs/policy.csv")
            sub = username
            act = 'write'
            if e.enforce(sub, dom, obj, act):
                for id in ids[:len(ids)-1].split(','):
                    casbin_rule.delete_rule_on_id(id)
                acs_policy_version.add_version()
                return json.dumps({'status': 'ok', "code": 200, 'message': 'success'})
            else:
                return json.dumps({'status': 'fail', 'code': 401, 'message': 'unauthorization operation'})
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
            return json.dumps({'status': 'fail', 'code': 500, 'message': str(e)})

if __name__ == "__main__":
    t1 = threading.Thread(target=syncPolicy, args=(dom,))
    logger.debug('start thread sync policy ...')
    t1.start()
    logger.debug('start run ...')
    app.run()