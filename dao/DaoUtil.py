# -*- coding: utf-8 -*-
import configparser # for python3
# import ConfigParser # for python2
import threading
import os

import MySQLdb

class DaoUtil:
    u"""DBへの接続を管理するクラス
    設定ファイルはdao/conf/dbconf.iniを参照する"""

    _instance = None
    _connection = None
    _lock = threading.Lock()

    def __init__(self):
        super().__init__()

    """ Singleton """
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)

        return cls._instance

    def getConnection(self):
        u"""コネクションがすでに確立されていれば、そのコネクションを返す。
        コネクションが未確立なら、コネクションを確立してそのコネクションを返す。"""
        if self._connection is None:
            inifile = configparser.ConfigParser()
            inifile.read(os.path.dirname(__file__) + "/conf/dbconf.ini")
            db = inifile.get("setting", "db")
            host = inifile.get("setting", "host")
            port = inifile.get("setting", "port")
            user = inifile.get("setting", "user")
            password = inifile.get("setting", "password")
            charset = inifile.get("setting", "charset")
            self._connection = MySQLdb.connect(db=db, host=host, port=int(port), user=user, passwd=password, charset=charset)
        return self._connection

    def __del__(self):
        u"""デストラクタ"""

        if self._connection is not None:
            try:
                self._connection.close()
            except MySQLdb.Error as e:
                pass