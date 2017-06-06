#!python3
#encoding:utf-8
import os.path
import subprocess
import database.src.license.insert.command.miscellaneous.Licenses
class Main:
    def __init__(self, db, client):
        self.__db = db
        self.__client = client
        self.__licenses = database.src.license.insert.command.miscellaneous.Licenses.Licenses(self.__db, self.__client)

    def Initialize(self):
        self.__InsertForFile()

    def Run(self):
        license_key = 'start'
        while '' != license_key:
            print('入力したKeyのライセンスを問い合わせます。(未入力+Enterで終了)')
            print('サブコマンド    l:既存リポジトリ m:一覧更新  f:ファイルから1件ずつ挿入')
            key = input()
            if '' == key:
                break
            elif 'l' == key or 'L' == key:
                self.__licenses.Show()
            elif 'f' == key or 'F' == key:
                self.__InsertForFile()
            elif 'm' == key or 'M' == key:
                self.__licenses.Update()
            else:
                self.__licenses.InsertOne(key)

    def __InsertForFile(self):
        file_name = 'LicenseKeys.txt'
        file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), file_name)
        if not(os.path.isfile(file_path)):
            print(file_name + 'ファイルを作成し、1行ずつキー名を書いてください。')
            return
        with open(file_path, mode='r', encoding='utf-8') as f:
            for line in f:
                print(line.strip())
                self.__licenses.InsertOne(line.strip())

