#!python3
#encoding:utf-8
import requests
import datetime
import time
import json
import web.service.github.api.v3.Response
class SshKeys(object):
    def __init__(self, reqp, response):
#    def __init__(self):
#        self.__response = web.service.github.api.v3.Response.Response()
        self.__reqp = reqp
        self.__response = response

    """
    SSH鍵の生成。
    @params {string} public_keyはSSH公開鍵。
    @params {string} titleはSSH公開鍵。
    """
    def Create(self, public_key, title=None):
#    def Create(self, mailaddress, public_key):
#    def Create(self, token, mailaddress, public_key):
        method = 'POST'
        endpoint = 'users/:username/keys'
        params = self.__reqp.Get(method, endpoint)
#        headers=self.__GetHeaders(token)
#        data=json.dumps({'title': mailaddress, 'key': public_key})
#        params['data'] = json.dumps({'title': mailaddress, 'key': public_key})
        params['data'] = json.dumps({'title': title, 'key': public_key})
        url = 'https://api.github.com/user/keys'
        print(url)
        print(data)
        r = requests.post(url, **params)
#        r = requests.post(url, headers=headers, data=data)
        return self.__response.Get(r)
        
    def Gets(self, username):
#    def Gets(self, username, token):
        method = 'GET'
        endpoint = 'users/:username/keys'
        params = self.__reqp.Get(method, endpoint)
        keys = []
        url = 'https://api.github.com/users/{username}/keys'.format(username=username)
#        headers=self.__GetHeaders(token)
        while None is not url:
            print(url)
#            r = requests.get(url, headers=headers)
            r = requests.get(url, **params)
            keys += self.__response.Get(r)
            url = self.__response.Headers.Link.Next(r)
            params = self.__reqp.Get(method, endpoint)
        return keys
        
    def Get(self, key_id):
#    def Get(self, token, key_id):
        method = 'GET'
        endpoint = 'user/keys/:id'
        params = self.__reqp.Get(method, endpoint)
        url = 'https://api.github.com/user/keys/{key_id}'.format(key_id=key_id)
#        headers=self.__GetHeaders(token)
        print(url)
        r = requests.get(url, **params)
#        r = requests.get(url, headers=headers)
        return self.__response.Get(r)
        
    """
    GitHubに設定したSSH公開鍵を削除する。
    BASIC認証でしか使えない。
    """
    def Delete(self, key_id):
#    def Delete(self, key_id, username, password, otp=None):
        method = 'DELETE'
        endpoint = 'user/keys/:id'
        params = self.__reqp.Get(method, endpoint)
        url = 'https://api.github.com/user/keys/{key_id}'.format(key_id=key_id)
#        headers=self.__GetHeaders(otp)
        print(url)
        r = requests.delete(url, **params)
#        r = requests.delete(url, headers=headers, auth=(username, password))
        return self.__response.Get(r)

    def __GetHeaders(self, token=None, otp=None):
        headers = {
            'Time-Zone': 'Asia/Tokyo',
            'Accept': 'application/vnd.github.v3+json'
        }
        if None is not token:
            headers.update({'Authorization': 'token ' + token})
        if None is not otp:
            headers.update({'X-GitHub-OTP': otp})
        print(headers)
        return headers
