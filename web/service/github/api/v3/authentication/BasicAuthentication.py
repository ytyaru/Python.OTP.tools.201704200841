#!python3
#encoding:utf-8
from web.service.github.api.v3.authentication.Authentication import Authentication
class BasicAuthentication(Authentication):
    def __init__(self, username, password):
        super().__init__()
        self.__username = username
        self.__password = password
    
    @property    
    def Username(self):
        return self.__username
    
    @property    
    def Password(self):
        return self.__password

    """
    requestsライブラリのAPIで使うheadersを生成する。
    """
    def GetHeaders(self):
        return super().GetHeaders()
    
    """
    requestsライブラリのAPIで使う**kwargsを生成する。
    requests.get(url, **this.GetRequestParameters())
    """
    def GetRequestParameters(self):
        params = super().GetRequestParameters()
        params.update({'auth': (self.__username, self.__password), 'headers': self.GetHeaders()})
        return params

