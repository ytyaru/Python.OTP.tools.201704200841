#!python3
#encoding:utf-8
import requests
import urllib.parse
import json
import web.service.github.api.v3.Response
class Repositories:
    def __init__(self, reqp, response, authData, repo):
#    def __init__(self, reqp, response, authData=None, repo=None):
#    def __init__(self, reqp, response, authData, repo):
#    def __init__(self, reqp, response, user, repo):
        self.__reqp = reqp
        self.__response = response
        self.__authData = authData
        self.__repo = repo

    def create(self, name, description=None, homepage=None):
        method = 'POST'
        endpoint = 'user/repos'
        params = self.__reqp.Get(method, endpoint)
#        params = self.__reqp.get(method, endpoint)
        params['data'] = json.dumps({"name": name, "description": description, "homepage": homepage})
        print(params)
#        r = requests.post(urllib.parse.urljoin("https://api.github.com", endpoint), headers=params['headers'], data=params['data'])
        r = requests.post(urllib.parse.urljoin("https://api.github.com", endpoint), **params)
        return self.__response.Get(r)
        
    def gets(self, visibility=None, affiliation=None, type=None, sort='full_name', direction=None, per_page=30):
        if (visibility is None) and (affiliation is None) and (type is None):
            type = 'all'
        self.__raise_param_error(visibility, ['all', 'public', 'private'], 'visibility')
        if not(None is affiliation):
            for a in affiliation.split(','):
                self.__raise_param_error(a, ['owner', 'collaborator', 'organization_member'], 'affiliation')
        self.__raise_param_error(type, ['all', 'owner', 'public', 'private', 'member'], 'type')
        self.__raise_param_error(sort, ['created', 'updated', 'pushed', 'full_name'], 'sort')
        if direction is None:
            if sort == 'full_name':
                direction = 'asc'
            else:
                direction = 'desc'
        else:
            self.__raise_param_error(direction, ['asc', 'desc'], 'direction')

        """
        method = 'GET'
        endpoint = 'user/repos'
        params = self.__reqp.Get(method, endpoint)
#        params = self.__reqp.get(method, endpoint)
        params['headers']['Accept'] = 'application/vnd.github.drax-preview+json'
        params['params'] = {}
        if not(None is visibility):
            params['params']["visibility"] = visibility
        if not(None is affiliation):
            params['params']["affiliation"] = affiliation
        if not(None is type):
            params['params']["type"] = type
        if not(None is sort):
            params['params']["sort"] = sort
        if not(None is direction):
            params['params']["direction"] = direction
        if not(None is per_page):
            params['params']["per_page"] = per_page
        print(params)
        """
#        params = self.__GetCreateParameter(visibility, affiliation, type, sort, direction, per_page)
        repos = []
        url = urllib.parse.urljoin('https://api.github.com', 'user/repos')
        while (None is not url):
            print(url)
#            params = self.__reqp.update_otp(params)
            params = self.__GetCreateParameter(visibility, affiliation, type, sort, direction, per_page)
            print(params)
            r = requests.get(url, **params)
#            r = requests.get(url, headers=params['headers'], params=json.dumps(params['params']))
            repos += self.__response.Get(r)
            url = self.__response.Headers.Link.Next(r)
        return repos

    def __GetCreateParameter(self, visibility=None, affiliation=None, type=None, sort='full_name', direction=None, per_page=30):
        method = 'GET'
        endpoint = 'user/repos'
        params = self.__reqp.Get(method, endpoint)
        print(params)
#        params = self.__reqp.get(method, endpoint)
        params['headers'].update({'Accept': 'application/vnd.github.drax-preview+json'})
#        params['headers']['Accept'] = 'application/vnd.github.drax-preview+json'
        print(params)

        params['params'] = {}
        if not(None is visibility):
            params['params']["visibility"] = visibility
        if not(None is affiliation):
            params['params']["affiliation"] = affiliation
        if not(None is type):
            params['params']["type"] = type
        if not(None is sort):
            params['params']["sort"] = sort
        if not(None is direction):
            params['params']["direction"] = direction
        if not(None is per_page):
            params['params']["per_page"] = per_page
        print(params)
        return params

    def __raise_param_error(self, target, check_list, target_name):
        if not(target is None) and not(target in check_list):
            raise Exception("Parameter Error: [{0}] should be one of the following values. : {1}".format(target_name, check_list))

    """
    公開リポジトリの一覧を取得する。
    @param [int] since is repository id on github.
    """
    def list_public_repos(self, since, per_page=30):
        method = 'GET'
        endpoint = 'repositories'
        params = self.__reqp.Get(method, endpoint)
#        params = self.__reqp.get(method, endpoint)
        params['params'] = json.dumps({"since": since, "per_page": per_page})
        print(params)
        r = requests.get(urllib.parse.urljoin("https://api.github.com", endpoint), **params)
#        r = requests.get(urllib.parse.urljoin("https://api.github.com", endpoint), headers=params['headers'])
        return self.__response.Get(r)

    """
    リポジトリを削除する。
    引数を指定しなければ、デフォルトユーザのカレントディレクトリ名リポジトリを対象とする。
    """
    def delete(self, username=None, repo_name=None):
        if None is username:
#            username = self.__user.Name
            username = self.__authData.Username
        if None is repo_name:
            repo_name = self.__repo.Name
        endpoint = 'repos/:owner/:repo'
        params = self.__reqp.Get('DELETE', endpoint)
#        params = self.__reqp.get('DELETE', endpoint)
        endpoint = endpoint.replace(':owner', username)
        endpoint = endpoint.replace(':repo', repo_name)
        r = requests.delete(urllib.parse.urljoin("https://api.github.com", endpoint), **params)
#        r = requests.delete(urllib.parse.urljoin("https://api.github.com", endpoint), headers=params['headers'])
        return self.__response.Get(r)

    """
    リポジトリを編集する。
    リポジトリ名、説明文、homepageを変更する。
    指定せずNoneのままなら変更しない。
    """
    def edit(self, name=None, description=None, homepage=None):
        if None is name:
#            name = self.__user.Name
            name = self.__repo.Name
        if None is description:
            description = self.__repo.Description
        if None is homepage:
            homepage = self.__repo.Homepage

        endpoint = 'repos/:owner/:repo'
        params = self.__reqp.Get('PATCH', endpoint)
#        params = {}
#        params['headers'] = self.__reqp.Get('PATCH', endpoint)
#        params['headers'] = self.__reqp.get_default(scopes=['repo'])
#        endpoint = endpoint.replace(':owner', self.__user.Name)
        endpoint = endpoint.replace(':owner', self.__authData.Username)
        endpoint = endpoint.replace(':repo', self.__repo.Name)
        params['data'] = {}
        params['data']['name'] = name
        if not(None is description or '' == description):
            params['data']['description'] = description
        if not(None is homepage or '' == homepage):
            params['data']['homepage'] = homepage
        params['data'] = json.dumps(params['data'])
        url = urllib.parse.urljoin("https://api.github.com", endpoint)
        print(url)
        print(params['headers'])
        print(params['data'])
#        r = requests.patch(url, headers=params['headers'], data=json.dumps(params['data']))
        r = requests.patch(url, **params)
        return self.__response.Get(r)
        
    """
    リポジトリのプログラミング言語とそのファイルサイズを取得する。
    @param  {string} usernameはユーザ名
    @param  {string} repo_nameは対象リポジトリ名
    @return {dict}   結果(JSON形式)
    """
    def list_languages(self, username=None, repo_name=None):
        if None is username:
#            username = self.__user.Name
            username = self.__authData.Username
        if None is repo_name:
            repo_name = self.__repo.Name

        endpoint = 'repos/:owner/:repo/languages'
        params = self.__reqp.Get('GET', endpoint)
#        params = self.__reqp.get('GET', endpoint)
        endpoint = endpoint.replace(':owner', username)
        endpoint = endpoint.replace(':repo', repo_name)
        r = requests.get(urllib.parse.urljoin("https://api.github.com", endpoint), **params)
#        r = requests.get(urllib.parse.urljoin("https://api.github.com", endpoint), headers=params['headers'])
        print(endpoint)
        return self.__response.Get(r)

