# -*- coding: utf-8 -*-

import MySQLdb

import os,sys
sys.path.append(os.getcwd() + "/../")
from dao.DaoUtil import DaoUtil
from models.Product import Product

class ProductDao:
    u"""productテーブルのDAOクラス"""

    def __init__(self):
        super().__init__()

    def getAllProduct(self):
        u""" productテーブルの情報を全て取得する """

        con = None
        cursor = None
        products = []
        try:
            sql = "SELECT * FROM product"
            daoUtil = DaoUtil()
            con = daoUtil.getConnection()
            cursor = con.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(sql)
            results = cursor.fetchall()

            for result in results:
                product = Product()
                product.id = result["id"]
                product.name = result["name"]
                product.price = result["price"]
                product.detail = result["detail"]
                product.imagepath = result["imagepath"]
                products.append(product)

        except MySQLdb.Error as e:
            pass
        finally:
            try:
                if cursor is not None:
                    cursor.close()
                    cursor = None
                # if con is not None:
                #     con.close()
                #     con = None
            except MySQLdb.Error as e:
                pass

        return products


    def addProduct(self, product):
        """ 引数に指定したproductを登録する """


    def updateProduct(self, id, product):
        """ productを更新する """


    def deleteProduct(self, id):
        """ productを削除する """


if __name__ == "__main__":
    print(ProductDao.getAllProduct.__doc__)
    productDao = ProductDao()
    products = productDao.getAllProduct()
    for product in products:
        print(product.id)
        print(product.name)
        print(product.detail)
