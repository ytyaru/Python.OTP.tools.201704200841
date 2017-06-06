#!python3
#encoding:utf-8
import os.path
import dataset
#from tkinter import Tk
class RequestParam:
    def __init__(self, db, authData):
#    def __init__(self, authData):
#    def __init__(self, db, user):
        self.__db = db
#        self.__user = user
        self.__authData = authData
        self.__auth_param = RequestParam.AuthParam(self.__db, self.__authData)
#        self.__auth_param = RequestParam.AuthParam(self.__authData)
#        self.__auth_param = RequestParam.AuthParam(self.__db, self.__user)
#        self.__params = None

    """
    デフォルトのHTTPヘッダを取得する。
    API用DBに問い合わせずに取得できる。
    @param {array} scopesはAPIに必要な権限。['repo',`delete_repo`]など。未設定ならScopeに関係なく適当なTokenを取得する。
    @return {dict} HTTPHeader。
    """
    def get_default(self, scopes=None):
        return {
            "Time-Zone": "Asia/Tokyo",
#            "Authorization": "token {0}".format(self.__user.GetAccessToken(scopes)),
            "Authorization": "token {0}".format(self.__authData.GetAccessToken(scopes)),
            "Accept": "application/vnd.github.v3+json",
        }

    """
    APIごとに適切なHttpHeaderを返す。
    * API毎に異なる認証方法(Basic,Token)(未実装:OAuth,TwoFactor)
    * API毎に異なる必要scope
    * API毎に異なる必要Accept(未実装)
    * アカウントと時刻ごとに異なるOTP(未実装)
    * 国ごとに異なるTimeZone(未実装)
    http_methodとendpointでAPIを一意に特定する。
    """
    def get(self, http_method=None, endpoint=None):
        params = self.__auth_param.get(http_method, endpoint)
        if not("headers" in params.keys()):
            params['headers'] = {}
        params['headers'].update({"Time-Zone": "Asia/Tokyo"})
        if not("Accept" in params['headers'].keys()):
            params['headers'].update({"Accept": "application/vnd.github.v3+json"})
        self.__params = params
        return self.__params

    """
    一定時間ごとに変化するワンタイムパスワード(OTP)を取得してHttpHeaderに設定する（未実装）
    """
    def update_otp(self, params):
        otp = self.__authData.OneTimePassword
        if None is not self.__params:
            if not('headers' in self.__params):
                self.__params['headers'] = {}
            if None is not otp:
                self.__params['headers']['X-GitHub-OTP'] = otp
        return self.__params
#        secret = self.__user.TwoFactorSecret
#        secret = self.__authData.TwoFactorSecret
        # SecretからOTPを算出する
        # X-GitHub-OTPヘッダキーにOTPを設定する
        """
        otp = self.__auth_param.get_otp()
        if None is otp:
            return params
        if None is not params:
            if not('headers' in params):
                params['headers'] = {}
            params['headers']['X-GitHub-OTP'] = otp
        """
#        return params
        
    class AuthParam:
        def __init__(self, db, authData):
#        def __init__(self, authData):
#        def __init__(self, db, user):
            self.__db = db
#            self.__user = user
            self.__authData = authData

        """
        APIごとに適切なHttpHeaderを返す。
        * API毎に異なる認証方法(Basic,Token)(未実装:OAuth,TwoFactor)
        * API毎に異なる必要scope
        * アカウントと時刻ごとに異なるOTP(未実装)
        """
        def get(self, http_method, endpoint):
            if False == self.__authData.IsBasicAuthenticatable() and False == self.__authData.IsTokenAuthenticatable():
                raise Exception('認証データが設定されていません。Username, Password, Token, 2FA-Secret, 認証方法に合わせて必要なものを設定してください。')
            params = {}
            account = self.__db.account['Accounts'].find_one(Username=self.__authData.Username)
#            account = self.__db.account['Accounts'].find_one(Username=self.__user.Name)
            api = self.__db.api['Apis'].find_one(HttpMethod=http_method.upper(), Endpoint=endpoint)
            if None is api:
                return __get_default_headers()
            print(api)
#            print(api['Grants'])
#            print("type(Grants)1: {0}".format(type(api['Grants'])))
#            print("len(Grants)1: {0}".format(len(api['Grants'])))
#            print("len(Grants)2: {0}".format(len(api['Grants'].split(","))))
                
            # APIはBasic,TokenどちらでもOKで、認証データも両方ある
            # APIがToken実行できて、認証データもTokenがある
            # APIがToken実行できるが、認証データがBASICデータしかない
            # APIがBasic実行しかできないが、認証データにBASICデータがない
            # APIがBasic実行しかできないが、認証データにBASICデータがある
            if ("Token" in api['AuthMethods']):
                if self.__authData.IsTokenAuthenticatable():
                    grants = api['Grants'].split(",")
                    if not(None is grants) and 0 == len(grants):
                        grants = None
                    if not(None is grants) and 1 == len(grants) and '' == grants[0]:
                        grants = None
                    token = self.__authData.GetAccessToken(grants)
                    params['headers'] = {"Authorization": "token " + token}
                else:
                    params['auth'] = (self.__authData.Username, self.__authData.Password)
                    if None is not self.__authData.OneTimePassword:
                        params['headers'] = {"X-GitHub-OTP": self.__authData.OneTimePassword}
            elif ("ClientId" in api['AuthMethods']):
                raise Exception('Not implemented clientId authorization.')
            elif ("Basic" in api['AuthMethods']):
                if self.__authData.IsBasicAuthenticatable():
                    params['auth'] = (self.__authData.Username, self.__authData.Password)
                    if None is not self.__authData.OneTimePassword:
                        params['headers'] = {"X-GitHub-OTP": self.__authData.OneTimePassword}
                else:
                    raise Exception('API {method} {api} の実行にはBASIC認証が必要ですが、認証データにUsernameとPasswordが設定されていません。2FA有効アカウントならTwoFactorSecretキーも必要です。'.format(method=api['HttpMethod'], api=api['Endpoint']))
            else:
                raise Exception('Not found AuthMethods: {0} {1}'.format(api['HttpMethod'], api['Endpoint']))
            return params
            """
            if ("Token" in api['AuthMethods']):
                grants = api['Grants'].split(",")
                if not(None is grants) and 0 == len(grants):
                    grants = None
                if not(None is grants) and 1 == len(grants) and '' == grants[0]:
                    grants = None
#                token = self.__user.GetAccessToken(grants)
                token = self.__authData.GetAccessToken(grants)
                params['headers'] = {"Authorization": "token " + token}
            elif ("ClientId" in api['AuthMethods']):
                raise Exception('Not implemented clientId authorization.')
            elif ("Basic" in api['AuthMethods']):
#                params['auth'] = (self.__username, account['Password'])
#                two_factor = self.__db.account['TwoFactors'].find(AccountId=account['Id'])
#                params['auth'] = (self.__user.Name, self.__user.Password)
                params['auth'] = (self.__authData.Username, self.__authData.Password)
                if None is not self.__authData.OneTimePassword:
#                if None is not self.__user.Otp:
#                    params['headers'] = {"X-GitHub-OTP": self.__user.Otp}
                    params['headers'] = {"X-GitHub-OTP": self.__authData.OneTimePassword}
#                two_factor = self.__db.account['TwoFactors'].find(AccountId=account['Id'])
#                if not(None is two_factor):
#                    t = Tk()
#                    otp = t.clipboard_get()
#                    t.destroy()
#                    otp = "some_otp"
#                    params['headers'] = {"X-GitHub-OTP": otp}
            else:
                raise Exception('Not found AuthMethods: {0} {1}'.format(api['HttpMethod'], api['Endpoint']))
            return params
            """

        """
        デフォルトのHTTPヘッダを取得する。
        @param {array} scopesはAPIに必要な権限。['repo',`delete_repo`]など。未設定ならScopeに関係なく適当なTokenを取得する。
        @return {dict} HTTPHeader。
        """
        def __get_default_headers(self, scopes=None):
            return {
                "Time-Zone": "Asia/Tokyo",
#                "Authorization": "token {0}".format(self.data.get_access_token(scopes)),
                "Authorization": "token {0}".format(self.__authData.GetAccessToken(scopes)),
                "Accept": "application/vnd.github.v3+json",
            }
