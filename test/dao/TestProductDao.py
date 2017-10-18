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

    def test_productDao_success1(self):
        products = self.productDao.getAllProduct()

        for product in products:
            assert isinstance(product, Product)