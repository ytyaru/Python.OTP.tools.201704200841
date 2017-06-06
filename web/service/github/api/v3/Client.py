#!python3
#encoding:utf-8
import web.http.Response
import web.service.github.api.v3.Response
#import web.service.github.api.v3.RequestParam
import web.service.github.api.v3.RequestParameter
from web.service.github.api.v3.miscellaneous.Licenses import Licenses
from web.service.github.api.v3.repositories.Repositories import Repositories
from web.service.github.api.v3.authorizations.Authorizations import Authorizations
from web.service.github.api.v3.users.Users import Users
from web.service.github.api.v3.users.SshKeys import SshKeys
from web.service.github.api.v3.users.Emails import Emails
class Client(object):
    def __init__(self, db, authentications, authData=None, repo=None):
        self.__db = db
        self.__repo = repo
        self.__authData = authData
#        self.__reqp = web.service.github.api.v3.RequestParam.RequestParam(self.__db, self.__authData)
        self.__reqp = web.service.github.api.v3.RequestParameter.RequestParameter(self.__db, authentications)
#        self.__reqp = web.service.github.api.v3.RequestParam.RequestParam(self.__db, self.__user)
        self.__response = web.service.github.api.v3.Response.Response()
        self.license = Licenses(self.__reqp, self.__response)
#        self.license = Licenses.Licenses(self.__reqp, self.__response)
        self.repo = Repositories(self.__reqp, self.__response, self.__authData, self.__repo)
#        self.repo = Repositories.Repositories(self.__reqp, self.__response, self.__authData, self.__repo)
#        self.repo = Repositories.Repositories(self.__reqp, self.__response, self.__user, self.__repo)
        self.authorization = Authorizations(self.__reqp, self.__response)
        self.user = Users(self.__reqp, self.__response)
        self.sshkey = SshKeys(self.__reqp, self.__response)
        self.email = Emails(self.__reqp, self.__response)
    @property
    def Repositories(self):
        return self.repo
    @property
    def Licenses(self):
        return self.license
    @property
    def Authorizations(self):
        return self.authorization
    @property
    def Users(self):
        return self.user
    @property
    def SshKeys(self):
        return self.sshkey
    @property
    def Emails(self):
        return self.email
