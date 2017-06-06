#!python3
#encoding:utf-8
import database.src.Database
import dataset
class AuthenticationData(object):
    def __init__(self):
        self.__username = None
        self.__password = None
        self.__mailaddress = None
        self.__two_factor_secret = None
        self.__otp = None
        self.__token = None
        self.__ssh_host = None

    def __GetUsername(self):
        return self.__username
    Username = property(__GetUsername)
    
    def __GetPassword(self):
        return self.__password
    Password = property(__GetPassword)
    
    def __GetMailAddress(self):
        return self.__mailaddress
    MailAddress = property(__GetMailAddress)
    
    def __GetTwoFactorSecret(self):
        return self.__two_factor_secret
    TwoFactorSecret = property(__GetTwoFactorSecret)
    
    def __GetOneTimePassword(self):
        return self.__otp
    OneTimePassword = property(__GetOneTimePassword)
    
    def __GetAccessToken(self):
        return self.__token
    AccessToken = property(__GetAccessToken)
    
    def __GetSshHost(self):
        return self.__ssh_host
    SshHost = property(__GetSshHost)
    
    """
    Basic認証できるか否か(UsernameとPasswordが設定されているか)
    """
    def IsBasicAuthenticatable(self):
        if None is self.__username or 0 == len(self.__username.strip()):
            return False
        if None is self.__password or 0 == len(self.__password.strip()):
            return False
        return True
    
    """
    Authentication認証できるか否か(AccessTokenが設定されているか)
    """
    def IsTokenAuthenticatable(self):
        if None is self.__token or 0 == len(self.__token.strip()):
            return False
        return True
    
    """
    認証用データを読み取る。`GitHub.Accounts.sqlite3`DBとユーザ名から。
    """
    def Load(self, db_account, username):
        account = db_account['Accounts'].find_one(Username=username)
        if None is account:
            raise Exception('指定したユーザ名 {user} はDBに存在しません。'.format(user=username))
        self.__username = account['Username']
        self.__password = account['Password']
        self.__mailaddress = account['MailAddress']
        two_factor = db_account['TwoFactors'].find_one(AccountId=account['Id'])
        if None is not two_factor:
            self.__two_factor_secret = two_factor['Secret']
            self.__otp = self.__CalcOneTimePassword() # OTP算出して設定する
        token = db_account['AccessTokens'].find_one(AccountId=account['Id'])
        if None is not token:
            self.__token = token['AccessToken']
        sshconfigures = db_account['SshConfigures'].find_one(AccountId=account['Id'])
        if None is not sshconfigures:
            self.__ssh_host = sshconfigures['HostName']

    """
    Basic認証用データを設定する。引数で直接。
    """
    def SetBasic(self, username, password, two_factor_secret=None):
        self.__username = username
        self.__password = password
        if None is not two_factor_secret:
            self.__two_factor_secret = two_factor_secret

    """
    OAuth認証用データを設定する。引数で直接。
    """
    def SetToken(self, token):
        self.__token = token
    
    def GetAccessToken(self, scopes=None):
#        sql = "SELECT * FROM AccessTokens WHERE AccountId == {0}".format(self.__account_id)
        sql = "SELECT * FROM AccessTokens WHERE AccountId == {0}".format(self.__db.account['Accounts'].find_one(Username=self.Username)['Id'])
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
        return ret['AccessToken']
#        return self.__db.account.query(sql).next()['AccessToken']

    """
    ワンタイムパスワードを算出して返す。
    """
    def __CalcOneTimePassword(self):
        # self.__two_factor_secret を使う
        return None
