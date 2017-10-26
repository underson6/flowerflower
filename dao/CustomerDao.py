# -*- coding: utf-8 -*-

import MySQLdb

import os,sys
sys.path.append(os.getcwd() + "/../")
from dao.DaoUtil import DaoUtil
from models.Customer import Customer

class CustomerDao:
    u""" CustomerテーブルのDAOクラス """

    def __init__(self):
        super().__init__()

    def getAllCustomer(self):
        u"""全ての顧客情報を取得する"""
        con = None
        cursor = None
        customers = []
        try:
            sql = "SELECT * FROM customer"
            daoUtil = DaoUtil()
            con = daoUtil.getConnection()
            cursor = con.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(sql)
            results = cursor.fetchall()

            for result in results:
                customer = Customer()
                customer.id = result["id"]
                customer.name = result["name"]
                customer.address= result["address"]
                customer.email = result["email"]
                customer.isMember = result["member"]
                customers.append(customer)

        except MySQLdb.Error as e:
            print(e)
        finally:
            try:
                # if con is not None:
                #     con.close()
                #     con = None
                if cursor is not None:
                    cursor.close()
                    cursor = None
            except MySQLdb.Error as e:
                print(e)

        return customers

    def addCustomer(self, customer):
        u"""顧客情報を追加する"""
        sql = "INSERT INTO customer VALUES (null, %s, %s, %s, %s)"
        con = None
        cursor = None
        isSuccess = False
        try:
            daoUtil = DaoUtil()
            con = daoUtil.getConnection()
            cursor = con.cursor()
            cursor.execute("SET CHARACTER SET utf8")
            cursor.execute(sql, (customer.name, customer.address, customer.email, int(customer.isMember)))
            con.commit()
            isSuccess = True
        except MySQLdb.Error as e:
            print(e)
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

        return isSuccess

if __name__ == "__main__":
    customer = Customer()
    customer.name = "ore"
    customer.email = "hoge@hoge.com"
    customer.address = "kanagawakenkawasakishi"
    customer.isMember = int(0)
    customerDao = CustomerDao()
    result = customerDao.addCustomer(customer)

    if result:
        print("insert ok")
    else:
        print("not inserted")


    customerDao = CustomerDao()
    customers = customerDao.getAllCustomer()
    print(len(customers))
    for customer in customers:
        print(customer.name)
        print(customer.address)
        print(customer.email)
        print()