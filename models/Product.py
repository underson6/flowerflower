# -*- coding: utf-8 -*-
class Product:
    """商品のモデルクラス"""

    def __init__(self):
        self.id = 0
        self.name = ""
        self.price = 0
        self.detail = ""
        self.tag = ""
        self.image = "/static/images/no_images.jpg"
