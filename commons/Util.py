# -*- coding: utf-8 -*-

import os, hashlib

class Util():
    u"""スタティックメソッドを集めた"""

    @staticmethod
    def getRandomStr():
        u"""urandomからSHA256を利用してランダムな文字列を取得する"""
        m = hashlib.sha256()
        m.update(os.urandom(64))
        randomStr = m.hexdigest()

        return randomStr
