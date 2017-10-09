# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for, session
from commons import randomMessage
from models.Product import Product
from models.Customer import Customer

from dao.ProductDao import ProductDao
from dao.CustomerDao import CustomerDao

app = Flask(__name__)
app.config["SECRET_KEY"] = "this is a secret key"

@app.before_request
def before_request():
    if session.get("username") is not None:
        print("logged in")
    if request.path == "/login":
        print("you want to go to login page")
        session["username"] = "ohana"
        # return render_template("index.html")
        return redirect(url_for("hello"))
        pass
    print("redirect")


@app.route("/")
def hello():
    title = u"ようこそ"
    # message = randomMessage.pick_up()
    productDao = ProductDao()
    products = productDao.getAllProduct()
    message = "hogehogeee"
    return render_template("index.html", title=title, message=message, products=products)
    # return "Hello Flask!"


@app.route("/search", methods=["GET", "POST"])
def post():
    title = u"こんにちは"
    if request.method == 'POST':
        # リクエストフォームから「名前」を取得して
        name = request.form['name']

        products = []
        products.append(Product())
        a = Product()
        a.price = 210
        products.append(a)

        # index.html をレンダリングする
        return render_template('index.html',
                               name=name, title=title, products=products)
    else:
        # エラーなどでリダイレクトしたい場合はこんな感じで
        return redirect(url_for('hello'))

if __name__ == "__main__":
    app.debug = False
    app.run(host="0.0.0.0")
