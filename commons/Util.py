# -*- coding: utf-8 -*-

import os, hashlib

class Util():

    @staticmethod
    def getRandomStr():
        m = hashlib.sha256()
        m.update(os.urandom(64))
        randomStr = m.hexdigest()

        return randomStr
