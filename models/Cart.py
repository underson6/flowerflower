# -*- coding: utf-8 -*-

class Cart():
    """Cartテーブルのモデル"""
    def __init__(self):
        self.sessionId = ""
        self.productId = 0
        self.count = 0
        self.price = 0
        self.amount = 0
        self.image = ""
        self.updateTime = ""
