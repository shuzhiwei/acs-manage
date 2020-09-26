import json, requests
import time, threading

lock = threading.RLock()
version = -1

def syncPolicy(domain):
    while True:
        global version
        lock.acquire()
        url = 'http://172.26.21.91:8082/api/v1/policy/version'
        con = requests.get(url).text
        d_con = json.loads(con)
        data = d_con['data']
        if version != data:
            url2 = 'http://172.26.21.91:8082/api/v1/policy/download?domain=' + domain
            con = requests.get(url2).text
            with open('confs/policy.csv', 'w') as f:
                f.write(con)
            version = data
        lock.release()
        time.sleep(60)

