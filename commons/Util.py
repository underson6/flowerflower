# -*- coding: utf-8 -*-

import os, hashlib
from PIL import Image

class Util():
    u"""スタティックメソッドを集めた"""

    @staticmethod
    def getRandomStr():
        u"""urandomからSHA256を利用してランダムな文字列を取得する"""
        m = hashlib.sha256()
        m.update(os.urandom(64))
        randomStr = m.hexdigest()

        return randomStr

    @staticmethod
    def createThumbnail(originalFilePath):
        u"""引数で渡されたパスにある画像ファイルのサムネイルを作成する"""

        _IMAGE_FILE_PATH = 'static/images/'
        img = Image.open(_IMAGE_FILE_PATH + originalFilePath)
        img.thumbnail(128, 128)
        img.save(_IMAGE_FILE_PATH + 'thumbnail/' + originalFilePath)
