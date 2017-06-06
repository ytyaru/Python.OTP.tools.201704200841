#!python3
#encoding:utf-8
import time
import pytz
import requests
import json
import datetime
class Licenses:
    def __init__(self, reqp, response):
        self.__reqp = reqp
        self.__response = response

    """
    全ライセンス情報を取得する。
    使用してみると一部ライセンスしか取得できない。CC0は取得できなかった。
    @return {array} ライセンス情報
    """
    def GetLicenses(self):
        licenses = []
        url = 'https://api.github.com/licenses'
        params = self.__reqp.Get('GET', 'licenses')
#        params = self.__reqp.get('GET', 'licenses')
        params['headers']['Accept'] = 'application/vnd.github.drax-preview+json'
        while (None is not url):
            r = requests.get(url, **params)
#            r = requests.get(url, headers=params['headers'])
            licenses += self.__response.Get(r)
            url = self.__response.Headers.Link.Next(r)
        return licenses

    """
    指定したライセンスの情報を取得する。
    @param  {string} keyはGitHubにおけるライセンスを指定するキー。
    @return {dict}   結果(JSON)
    """
    def GetLicense(self, key):
        url = 'https://api.github.com/licenses/' + key
        params = self.__reqp.Get('GET', 'licenses/:license')
#        params = self.__reqp.get('GET', 'licenses/:license')
        params['headers']['Accept'] = 'application/vnd.github.drax-preview+json'
        r = requests.get(url, **params)
#        r = requests.get(url, headers=params['headers'])
        return self.__response.Get(r)

    """
    リポジトリのライセンスを取得する。
    @param  {string} usernameはユーザ名
    @param  {string} repo_nameは対象リポジトリ名
    @return {dict}   結果(JSON形式)
    """
    def GetRepositoryLicense(self, username, repo_name):
        url = 'https://api.github.com/repos/{0}/{1}'.format(username, repo_name)
        params = self.__reqp.Get('GET', 'repos/:owner/:repo')
#        params = self.__reqp.get('GET', 'repos/:owner/:repo')
        params['headers']['Accept'] = 'application/vnd.github.drax-preview+json'
        r = requests.get(url, **params)
#        r = requests.get(url, headers=params['headers'])
        return self.__response.Get(r)

