#!python3
#encoding:utf-8
from web.service.github.api.v3.authentication.Authentication import Authentication
class NonAuthentication(Authentication):
    def __init__(self):
        pass
    """
    requestsライブラリのAPIで使うheadersを生成する。
    """
    def GetHeaders(self):
        return super().GetHeaders()
    """
    requestsライブラリのAPIで使う**kwargsを生成する。
    requests.get(url, **(this.GetRequestParameters()))
    """
    def GetRequestParameters(self):
        return super().GetRequestParameters()
