# -*- coding: utf-8 -*-
from nose.tools import with_setup, raises

import MySQLdb
from dao.ProductDao import ProductDao
from models.Product import Product

class TestProductDao():
    productDao = None

    def setup(self):
        self.productDao = ProductDao()

    def teardown(self):
        if self.productDao is not None:
            self.productDao = None

    def test_getAllProduct_success1(self):
        u"""getAllProduct正常系"""
        products = self.productDao.getAllProduct()

        for product in products:
            assert isinstance(product, Product)


    def test_getProductDetail_success1(self):
        u"""getProductDetail正常系"""
        product = self.productDao.getProductDetail(1)

        assert product.name == "hoge"
        assert product.detail == "hogehoge"
        assert product.price == 2000
        assert product.recommend == False
        assert product.tag == "aaa"
        assert product.image == None


    def test_getProductDetail_fail1(self):
        u"""存在しないid"""
        product = self.productDao.getProductDetail(100)

        assert product == None


    def test_getProductDetail_fail2(self):
        u"""idに文字列"""
        product = self.productDao.getProductDetail('a')

        assert product == None


    @raises(AssertionError)
    def test_getProductDetail_fail3(self):
        u"""SQLインジェクションができないこと"""

        u"""SQLの暗黙的な型変換でエラーが投げられるみたい"""
        product = self.productDao.getProductDetail("1 OR 1=1")

        assert product == None


    def test_getRecommendProduct_success(self):
        u"""getRecommendProductの正常系"""
        products = self.productDao.getRecommendProduct()

        assert products[0].name == "gaba"
        assert products[0].detail == "gabagaba"
        assert products[0].price == 2000
        assert products[0].recommend == True
        assert products[1].tag == ""
        assert products[1].image == "rose.jpg"

        assert products[1].name == "gaba"
        assert products[1].detail == "gabagaba"
        assert products[1].price == 2000
        assert products[1].recommend == True
        assert products[0].tag == "ccc"
        assert products[0].image == None


    def test_addProduct_succes(self):
        u"""addProductの正常系"""
        product = Product()
        product.name = ""
        product.price = 0
        product.detail = ""
        product.tag = ""
        product.image = ""
        recommend = 0

        # 追加前の件数を取得
        products_pre = self.productDao.getAllProduct()

        self.productDao.addProduct(product, recommend)

        # 追加後の件数を取得
        products_post = self.productDao.getAllProduct()

        assert len(products_post) == len(products_pre) + 1
