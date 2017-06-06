#!python3
#encoding:utf-8
import requests
import urllib.parse
#import json
class Requester:
    def __init__(self):
        pass
#    def __init__(self, db, authentications):
#        self.__db = db
#        self.__authentications = authentications
#        self.__reqp = RequestParameter(db, authentications)
        
    # postするdataをPythonメソッドから作成する処理が欲しい
    # APIごとに異なる引数とその型をもつ。それを`json.dumps(data)`して引数に渡す。
    def __CreateRequest(self, http_method, url, **params):
        req = requests.Request(http_method, url, **params)
    def Request(self, http_method, url, **req_params):
#    def Request(self, http_method, url, **req_params):
        # http://docs.python-requests.org/en/master/api/#lower-level-classes
#        req = requests.Request(http_method, url, **params)
#        req_params = self.__reqp.Get(http_method, endpoint)
        print(http_method)
        print(url)
        print(req_params)
        method = http_method
        url = url
        headers = None
        files = None
        data = None
        params = None
        auth = None
        cookies = None
        hooks = None
#        json = None
        if 'headers' in req_params:
            headers = req_params['headers']
        if 'files' in req_params:
            files = req_params['files']
        if 'data' in req_params:
            data = req_params['data']
        if 'params' in req_params:
            params = req_params['params']
        if 'auth' in req_params:
            auth = req_params['auth']
        if 'cookies' in req_params:
            cookies = req_params['cookies']
        if 'hooks' in req_params:
            hooks = req_params['hooks']
#        if 'json' in req_params:
#            json = req_params['json']
        req = requests.Request(method=http_method, url=url, headers=headers, files=files, data=data, params=params, auth=auth, cookies=cookies, hooks=hooks)
#        req = requests.Request(method=http_method, url=url, headers=headers, files=files, data=data, params=params, auth=auth, cookies=cookies, hooks=hooks, json=json)
        preq = req.prepare()
        s = requests.Session()
        res = s.send(preq)
        print(res.text)
        return res

        """
        if 'headers' in params:
            # getで引数をparamsに設定したとき
            if 'params' in params:
                if 'auth' in params:
                    req = requests.Request(http_method, url, headers=params['headers'], params=params['params'], auth=params['auth'])
                else:
                    req = requests.Request(http_method, url, headers=params['headers'], params=params['params'])
            # post, patch
            elif 'data' in params:
                if 'auth' in params:
                    req = requests.Request(http_method, url, headers=params['headers'], data=params['data'], auth=params['auth'])
                else:
                    req = requests.Request(http_method, url, headers=params['headers'], data=params['data'])
            # get, deleteで引数がないとき
            else:
                if 'auth' in params:
                    req = requests.Request(http_method, url, headers=params['headers'], auth=params['auth'])
                else:
                    req = requests.Request(http_method, url, headers=params['headers'])
        """
