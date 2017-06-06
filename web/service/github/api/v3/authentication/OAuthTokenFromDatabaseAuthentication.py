#!python3
#encoding:utf-8
from abc import ABCMeta, abstractmethod
from web.service.github.api.v3.authentication.OAuthAuthentication import OAuthAuthentication
class OAuthTokenFromDatabaseAuthentication(OAuthAuthentication):
    def __init__(self, db, username):
        self.__db = db
        self.__username = username
        self.SetAccessToken()
        super().__init__(self.__token)
    
    def SetAccessToken(self, scopes=None):
        sql = "SELECT * FROM AccessTokens WHERE AccountId == {0}".format(self.__db.account['Accounts'].find_one(Username=self.__username)['Id'])
        if not(None is scopes) and isinstance(scopes, list) and 0 < len(scopes):
            sql = sql + " AND ("
            for s in scopes:
                sql = sql + "(',' || Scopes || ',') LIKE '%,{0},%'".format(s) + " OR "
            sql = sql.rstrip(" OR ")
            sql = sql + ')'
#        print(scopes)
#        print(sql)
        res = self.__db.account.query(sql)
        ret = None
        for r in res:
#            print(r)
            ret = r
        if None is ret:
            raise Exception('指定されたScope {scopes} のうち少なくとも1つを持ったTokenが存在しません。: username={username}'.format(scopes=scopes, username=self.__username))
            # このときTokenを生成するAPIを使うにはパスワードが必要。Basic認証でないと使えない
        self.__token = ret['AccessToken']
#        print(self.__token)
        return self.__token
#        self.__token = self.__db.account.query(sql).next()['AccessToken']
#        return self.__db.account.query(sql).next()['AccessToken']

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
        return super().GetRequestParameters()

