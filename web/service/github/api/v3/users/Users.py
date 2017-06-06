#!python3
#encoding:utf-8
import requests
import datetime
import time
import json
import web.service.github.api.v3.Response
class Users:
    def __init__(self, reqp, response):
#    def __init__(self, username, password):
#        self.__username = username
#        self.__password = password
#        self.__response = web.service.github.api.v3.Response.Response()
        self.__reqp = reqp
        self.__response = response
        
    def Get(self):
#    def Get(self, username=None, password=None, otp=None):
#        if None is username:
#            username = self.__username
#        if None is password:
#            password = self.__password
        method = 'GET'
        endpoint = 'users/:username'
        params = self.__reqp.Get(method, endpoint)
        url = 'https://api.github.com/users/{username}'.format(username=username)
        print(url)
#        print('username: {0}'.format(username))
#        print('password: {0}'.format(password))
#        print('otp: {0}'.format(otp))
        r = requests.get(url, **params)
#        r = requests.get(url, headers=self.__GetHeaders(otp), auth=(username, password))
        return self.__response.Get(r)
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
