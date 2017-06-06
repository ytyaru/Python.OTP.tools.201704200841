#!python3
#encoding:utf-8
from abc import ABCMeta, abstractmethod
from web.service.github.api.v3.authentication.Authentication import Authentication
class OAuthAuthentication(Authentication):
    def __init__(self, token):
        super().__init__()
        self.__token = token
        if None is token:
            raise Exception('tokenはNoneにできません。有効なAccessToken文字列を指定してください。')
        
    @property
    def AccessToken(self):
        return self.__token

    """
    requestsライブラリのAPIで使うheadersを生成する。
    """
    def GetHeaders(self):
        headers = super().GetHeaders()
        headers.update({"Authorization": "token " + self.AccessToken})
        return headers

    """
    requestsライブラリのAPIで使う**kwargsを生成する。
    requests.get(url, **this.GetRequestParameters())
    """
    def GetRequestParameters(self):
        params = super().GetRequestParameters()
        params.update({'headers': self.GetHeaders()})
        return params

