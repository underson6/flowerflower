# -*- coding: utf-8 -*-

import MySQLdb
import os,sys
sys.path.append(os.getcwd() + "/../")
from dao.DaoUtil import DaoUtil
from models.Cart import Cart

class CartDao:
    u""" cartテーブルのDAOクラス """

    def __init__(self):
        super().__init__()

    def getCart(self, sessionId):
        u""" セッションIDに紐づいたカートの情報を取得する """
        con = None
        cursor = None
        cartItems = []
        try:
            sql = """
                SELECT cart.product_id as id, cart.count as count, product.price as price, cart.count * product.price as amount FROM cart 
                LEFT JOIN product 
                ON cart.product_id = product.id 
                WHERE session_id = %(id)s
                """
            daoUtil = DaoUtil()
            con = daoUtil.getConnection()
            cursor = con.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(sql,{"id":sessionId})
            results = cursor.fetchall()

            for result in results:
                cart = Cart()
                cart.productId = result["id"]
                cart.count = result["count"]
                cart.price = result["price"]
                cart.amount = result["amount"]
                cartItems.append(cart)

        except MySQLdb.Error as e:
            print(e)
        finally:
            try:
                if cursor is not None:
                    cursor.close()
                    cursor = None
            except MySQLdb.Error as e:
                print(e)

        return cartItems


    def addCart(self, sessionId, id, count):
        u"""カートに商品を追加する"""
        con = None
        cursor = None
        isSuccess = False
        try:
            sql = "INSERT INTO cart (session_id, product_id, count) values (%s, %s, %s)"
            daoUtil = DaoUtil()
            con = daoUtil.getConnection()
            cursor = con.cursor()
            cursor.execute("SET CHARACTER SET utf8")
            cursor.execute(sql, (sessionId, id, int(count)))
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


    def updateCart(self, sessionId, id, count):
        u"""商品の個数を更新する"""
        con = None
        cursor = None
        isSuccess = False
        try:
            sql = "UPDATE cart SET count = %s WHERE sessoin_id = %s AND product_id = %s"
            daoUtil = DaoUtil()
            con = daoUtil.getConnection()
            cursor = con.cursor()
            cursor.execute("SET CHARACTER SET utf8")
            cursor.execute(sql, (int(count), sessionId, id))
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


    def deleteCartItem(self, sessionId, id):
        u"""カートの商品を削除する"""
        con = None
        cursor = None
        isSuccess = False
        try:
            sql = "DELETE cart WHERE session_id = %s AND product_id = %s"
            daoUtil = DaoUtil()
            con = daoUtil.getConnection()
            cursor = con.cursor()
            cursor.execute("SET CHARACTER SET utf8")
            cursor.execute(sql, (sessionId, id))
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



if __name__ == "__main__":
    cartDao = CartDao()
    cartDao.addCart("hogehoge", 1, 1)


    print("hogehogehogehoge")
    cartDao = CartDao()
    carts = cartDao.getCart("hogehoge")
    for cartItems in carts:
        print(cartItems.productId)
        print(cartItems.count)
        print(cartItems.price)
        print(cartItems.amount)
