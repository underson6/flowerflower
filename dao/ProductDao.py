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
                product.image = result["image"]
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


    def getProductDetail(self, productId):
        u""" productテーブルから指定されたIDの情報を全て取得する """

        con = None
        cursor = None
        product = None
        try:
            sql = "SELECT * FROM product WHERE id = %(id)s"
            daoUtil = DaoUtil()
            con = daoUtil.getConnection()
            cursor = con.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(sql, {"id":productId})
            results = cursor.fetchall()

            for result in results:
                product = Product()
                product.id = result["id"]
                product.name = result["name"]
                product.price = result["price"]
                product.detail = result["detail"]
                product.image = result["image"]

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

        return product


    def getRecommendProduct(self):
        u""" productテーブルから指定されたIDの情報を全て取得する """

        con = None
        cursor = None
        products = []
        try:
            sql = "SELECT * FROM product WHERE recommend = 1"
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
                product.image = result["image"]
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


    def addProduct(self, product, recommend):
        """ 引数に指定したproductを登録する """
        con = None
        cursor = None
        isSuccess = False
        try:
            sql = "INSERT INTO product (name, detail, price, recommend, image) VALUES (%s, %s, %s, %s, %s);"
            daoUtil = DaoUtil()
            con = daoUtil.getConnection()
            cursor = con.cursor()
            cursor.execute("SET CHARACTER SET utf8")
            cursor.execute(sql, (product.name, product.detail, int(product.price), int(recommend), product.image))
            con.commit()
            isSuccess = True
        except MySQLdb.Error as e:
            print(e)
        finally:
            try:
                if cursor is not None:
                    cursor.close()
                    cursor = None
            except MySQLdb.Error as e:
                print(e)

        return isSuccess


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


    product = Product()
    product.name = "hogeeee"
    product.price = 50000
    product.detail = "hogehogehogehoge"
    product.image = ""
    productDao.addProduct(product, 1)