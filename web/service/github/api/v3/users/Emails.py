#!python3
#encoding:utf-8
import requests
import datetime
import time
import json
import web.service.github.api.v3.Response
class Emails(object):
    def __init__(self, reqp, response):
#    def __init__(self):
#        self.__response = web.service.github.api.v3.Response.Response()
        self.__reqp = reqp
        self.__response = response
    """
    メールアドレスを習得する。
    https://developer.github.com/v3/users/emails/#list-email-addresses-for-a-user
    @param {string} token。`user:email`権限をもったAccessTokenであること。
    """
    def Gets(self):
#    def Gets(self, token):
        method = 'GET'
        endpoint = 'user/emails'
        params = self.__reqp.Get(method, endpoint)
        print(params)
        url = 'https://api.github.com/user/emails'
        mails = []
        while None is not url:
            print(url)
#            headers=self.__GetHeaders(token)
            r = requests.get(url, **params)
#            r = requests.get(url, headers=headers)
            mails += self.__response.Get(r)
            url = self.__response.Headers.Link.Next(r)
            params = self.__reqp.Get(method, endpoint)
        return mails
    """
    def __GetHeaders(self, token, otp=None):
        method = 'POST'
        endpoint = 'users/:username/keys'
        params = self.__reqp.Get(method, endpoint)
        headers = {
            'Time-Zone': 'Asia/Tokyo',
            'Accept': 'application/vnd.github.v3+json',
            'Authorization': 'token ' + token
        }
        if None is not otp:
            headers.update({'X-GitHub-OTP': otp})
        print(headers)
        return headers
    """
