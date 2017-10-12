# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for, session
from commons import randomMessage
from models.Product import Product
from models.Customer import Customer

from dao.ProductDao import ProductDao
from dao.CustomerDao import CustomerDao
from dao.CartDao import CartDao

import json, random, os, hashlib

app = Flask(__name__)
app.config["SECRET_KEY"] = "this is a secret key"


@app.before_request
def before_request():
    print(session)
    if session.get('sessionid') is None:
        print("set session id")
        m = hashlib.sha256()
        m.update(os.urandom(64))
        randomStr = m.hexdigest()
        session["sessionid"] = randomStr
    else:
        print("session exist")

    print("##### " + session.get("sessionid") + " #####")


@app.route("/")
def hello():
    """topページを表示"""
    title = u"ようこそ"
    # message = randomMessage.pick_up()
    productDao = ProductDao()
    products = productDao.getAllProduct()
    sample = random.sample(products, 3)
    message = "hogehogeee"
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


@app.route("/cart/add", methods=["POST"])
def cartAdd():
    """カート画面を表示"""

    title = u"カート画面"

    productId = 0
    count = 0

    try:
        if request.form["productId"] is not None and request.form["productId"] != "":
            productId = int(request.form["productId"])
        else:
            pass
        if request.form["count"] is not None and request.form["count"] != "":
            count = int(request.form["count"])
        else:
            pass
    except TypeError as e:
        print(e)
        # error page

    isSuccess = False
    isExist = False

    cartDao = CartDao()
    isExist = cartDao.isExistProduct(session.get("sessionid"), productId)

    if isExist and productId > 0:
        print("update")
        isSuccess = cartDao.updateCart(session.get("sessionid"), productId, count)
    elif isExist is False and productId > 0:
        print("insert")
        isSuccess = cartDao.addCart(session.get("sessionid"), productId, count)



    message = ""
    if isSuccess:
        message = u"商品をカートに追加しました"
    else:
        message = u"カート追加に失敗しました。管理者にお問い合わせください。"

    """
    idがあればカートに入れる
    message=商品を追加しました的なメッセージ
    
    カートの全ての商品を表示する
    """

    # 空文字列チェック
    # if request.form["productId"] is None or request.form["productId"] == "":
    # # if None in [request.form("productId")]:
    #     pass
    # if isinstance(request.form["productId"], int) == False:
    #     pass

    # productId = request.form["productId"]
    # print("#############"+productId)
    # productDao = ProductDao()
    # products = productDao.getProductDetail(productId)
    # session["product"] = json.dumps(products.__dict__)
    # product = json.loads(session["product"])
    # for i in product:
    #     print(isinstance(i, int))
    # print("######################")

    return redirect(url_for("cart"))


@app.route("/cart")
def cart():
    """カート画面"""
    title = u"カート画面"

    cartDao = CartDao()
    cartItems = cartDao.getCart(session.get("sessionid"))

    amount = 0
    for cartItem in cartItems:
        amount += cartItem.amount

    return render_template("cart.html", title=title, cartItems=cartItems, amount=amount)


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
    app.debug = True
    app.run(host="0.0.0.0")
