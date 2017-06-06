#!python3
#encoding:utf-8
import sys
import subprocess
import shlex
import os.path
import getpass
import dataset
import database.src.TsvLoader
class Main:
    def __init__(self, db_path):
        self.__db_path = db_path
        self.__path_this_dir = os.path.abspath(os.path.dirname(__file__))
    def Run(self):
        self.__Create()
        self.__Insert()
    
    def __Create(self):
        subprocess.call(shlex.split("bash \"{0}\" \"{1}\"".format(os.path.join(self.__path_this_dir, "Create.sh"), self.__db_path)))
        
    def __Insert(self):
        name_table = "Colors"
        path_tsv = os.path.join(self.__path_this_dir, "{0}.tsv".format(name_table))
        loader = database.src.TsvLoader.TsvLoader()
        loader.ToSqlite3(path_tsv, self.__db_path, name_table)

