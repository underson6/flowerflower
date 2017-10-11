# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for, session
from commons import randomMessage
from models.Product import Product
from models.Customer import Customer

from dao.ProductDao import ProductDao
from dao.CustomerDao import CustomerDao

import json, random, os, hashlib

app = Flask(__name__)
app.config["SECRET_KEY"] = "this is a secret key"


@app.before_request
def before_request():
    if session is None:
        print("not have session")
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
    """topページを表示"""
    title = u"ようこそ"
    # message = randomMessage.pick_up()
    productDao = ProductDao()
    products = productDao.getAllProduct()
    sample = random.sample(products, 3)
    message = "hogehogeee"
    m = hashlib.sha256()
    m.update(os.urandom(64))
    print(m.hexdigest())
    return render_template("index.html", title=title, message=message, products=sample)
    # return "Hello Flask!"


@app.route("/all", methods=["GET", "POST"])
def all():
    """全商品表示画面を表示"""
    title = u"こんにちは"

    productDao = ProductDao()
    products = productDao.getAllProduct()

    # index.html をレンダリングする
    return render_template('all_products.html',
                           title=title, products=products)

@app.route("/detail/<int:id>", methods=["GET", "POST"])
def detail(id):
    """商品詳細画面を表示"""
    title = u"商品詳細画面"
    product = None
    productDao = ProductDao()
    product = productDao.getProductDetail(id)

    return render_template('detail.html', title=title, product=product)


@app.route("/recommend", methods=["GET", "POST"])
def recommend():
    """お勧め画面を表示"""
    title = u"お勧め商品"
    productDao = ProductDao()
    products = productDao.getRecommendProduct()

    return render_template('recommend.html', title=title, products=products)

    pass


@app.route("/cart", methods=["GET", "POST"])
def cart():
    """カート画面を表示"""

    title = "カート画面"

    """sessionに商品を入れる"""
    if session.get("products") is None:
        print("session products is None")
    else:
        print("session products is not None")

    # 空文字列チェック
    if request.form["productId"] is None or request.form["productId"] == "":
    # if None in [request.form("productId")]:
        # todo: エラーページに飛ばす
        pass
    if isinstance(request.form["productId"], int) == False:
        # todo: エラーページに飛ばす
        pass

    productId = request.form["productId"]
    print("#############"+productId)
    productDao = ProductDao()
    products = productDao.getProductDetail(productId)
    session["product"] = json.dumps(products.__dict__)
    product = json.loads(session["product"])
    for i in product:
        print(isinstance(i, int))
    print("######################")

    return render_template("cart.html", title=title)


@app.route("/orderInput")
def orderInput():
    """注文情報入力画面を表示"""
    pass


@app.route("/orderConfirm")
def orderConfirm():
    """注文情報確認画面を表示"""
    pass


@app.route("/orderComplete")
def orderComplete():
    """注文完了画面を表示"""
    pass


@app.route("/about")
def about():
    """このサイトについてを表示"""
    title = u"このサイトについて"
    return render_template("about.html", title=title)


@app.errorhandler(404)
def not_found(error):
    """404ページ"""
    pass


if __name__ == "__main__":
    app.debug = False
    app.run(host="0.0.0.0")
