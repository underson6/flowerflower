# -*- coding: utf-8 -*-
class Product:
    """商品のモデルクラス"""

    def __init__(self):
        self.id = 0
        self.name = u"おはな"
        self.price = 200
        self.detail = u"これはおはなです"
        self.image = "/static/images/no_images.jpg"
