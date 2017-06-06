#!python3
#encoding:utf-8
from abc import ABCMeta, abstractmethod
class Authentication(metaclass=ABCMeta):
    """
    requestsライブラリのAPIで使うheadersを生成する。
    """
    @abstractmethod
    def GetHeaders(self):
        return  {
            'User-Agent': '', # https://developer.github.com/v3/#user-agent-required
            'Accept': 'application/vnd.github.v3+json', # https://developer.github.com/v3/#current-version
            'Time-Zone': 'Asia/Tokyo', # https://developer.github.com/v3/#timezones
        }

    """
    requestsライブラリのAPIで使う**kwargsを生成する。
    requests.get(url, **(this.GetRequestParameters()))
    """
    @abstractmethod
    def GetRequestParameters(self):
        return {
            'headers': self.GetHeaders()
        }
