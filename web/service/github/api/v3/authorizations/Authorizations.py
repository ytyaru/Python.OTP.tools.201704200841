#!python3
#encoding:utf-8
import requests
import datetime
import time
import json
import web.service.github.api.v3.Response
class Authorizations:
    def __init__(self, reqp, response):
#    def __init__(self, username, password):
#        self.__username = username
#        self.__password = password
#        self.__response = web.service.github.api.v3.Response.Response()
        self.__reqp = reqp
        self.__response = response

    def Create(self, scopes=None, note=None, note_url=None, client_id=None, client_secret=None, fingerprint=None):
#    def Create(self, username=None, password=None, otp=None, scopes=None, note=None, note_url=None, client_id=None, client_secret=None, fingerprint=None):
#        if None is username:
#            username = self.__username
#        if None is password:
#            password = self.__password
        if not(self.__IsValidGrants(scopes)):
            raise Exception("invalid grant names.: {0}\n  use from the following. : {1}".format(scopes, self.__GetGrants()))
        if note is None:
            note = "token_note_{0:%Y%m%d%H%M%S%f}".format(datetime.datetime.now())
        data = {"note": note}
        if None is not scopes:
            data.update({"scopes": scopes})
        if None is not note_url:
            data.update({"note_url": note_url})
        if None is not client_id:
            data.update({"client_id": client_id})
        if None is not client_secret:
            data.update({"client_secret": client_secret})
        if None is not fingerprint:
            data.update({"fingerprint": fingerprint})

        method = 'POST'
        endpoint = 'authorizations'
        params = self.__reqp.Get(method, endpoint)
        params['data'] = json.dumps(data)
        url = 'https://api.github.com/' + endpoint
        print(url)
        print(params)
        r = requests.post(url, **params)
        """
        url = 'https://api.github.com/authorizations'
        headers = self.__GetHeaders(otp)
        print(url)
        print(headers)
        print(username)
        print(password)
        r = requests.post(url, headers=headers, auth=(username, password), data=json.dumps(data))
        """
        return self.__response.Get(r)

    def Gets(self):
#    def Gets(self, username=None, password=None, otp=None):
#        if None is username:
#            username = self.__username
#        if None is password:
#            password = self.__password
        method = 'GET'
        endpoint = 'authorizations'
        url = 'https://api.github.com/' + endpoint
        params = self.__reqp.Get(method, endpoint)
        print(url)
        print(params)
        r = requests.get(url, **params)
#        r = requests.get(url, headers=self.__GetHeaders(otp), auth=(username, password))
        return self.__response.Get(r)
        
    def Get(self, auth_id):
        """
    def Get(self, auth_id, username=None, password=None, otp=None):
        if None is username:
            username = self.__username
        if None is password:
            password = self.__password
        """
        method = 'GET'
        endpoint = 'authorizations/:id'
        params = self.__reqp.Get(method, endpoint)
        url = 'https://api.github.com/authorizations/{0}'.format(auth_id)
        print(url)
        print(params)
        r = requests.get(url, **params)
#        r = requests.get(url, headers=self.__GetHeaders(otp), auth=(username, password))
        return self.__response.Get(r)

    def Delete(self, auth_id):
#    def Delete(self, auth_id, username=None, password=None, otp=None):
        method = 'DELETE'
        endpoint = 'authorizations/:id'
        params = self.__reqp.Get(method, endpoint)
        url = 'https://api.github.com/authorizations/{auth_id}'.format(auth_id=auth_id)
#        headers = self.__GetHeaders(otp)
        print(url)
        print(params)
        r = requests.delete(url, **params)
#        r = requests.delete(url, headers=headers, auth=(username, password))
        return self.__response.Get(r)

    def __GetGrants(self):
        return ['repo', 'repo:status', 'repo_deployment', 'public_repo', 'admin:org', 'write:org', 'read:org', 'admin:public_key', 'write:public_key', 'read:public_key', 'admin:repo_hook', 'write:repo_hook', 'read:repo_hook', 'admin:org_hook', 'gist', 'notifications', 'user', 'user:email', 'user:follow', 'delete_repo', 'admin:gpg_key', 'write:gpg_key', 'read:gpg_key']

    def __IsValidGrants(self, grants):
        return all(grant in self.__GetGrants() for grant in grants)
        """
        for actual in grants:
            is_valid = False
            for expect in self.GetGrants():
                if actual == expect:
                    is_valid = True
                    break
            if not(is_valid):
                print('invalid grant name: %s'.format(actual))
                return False
        return True
        """
    """
    def __GetHeaders(self, otp=None):
        headers = {
            'Time-Zone': 'Asia/Tokyo',
            'Accept': 'application/vnd.github.v3+json',
        }
        if None is not otp:
            headers.update({'X-GitHub-OTP': otp})
        print(headers)
        return headers
    """
