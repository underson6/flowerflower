# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for, session
from commons import randomMessage
from commons import validationUtil
from commons.Util import *
from models.Product import Product
from models.Customer import Customer

from dao.ProductDao import ProductDao
from dao.CustomerDao import CustomerDao
from dao.CartDao import CartDao

import json, random, os, hashlib, shutil, zipfile, socket
from werkzeug import secure_filename

app = Flask(__name__)
app.config["SECRET_KEY"] = "this is a secret key"

"""
画像をアップロードするための一時フォルダ
同じファイル名の画像があった場合に不整合が発生するために
以下のディレクトリを使用
"""
app.config["UPLOAD_FOLDER"] = "static/images/tmp/"


@app.before_request
def before_request():
    u"""リクエストを受け取るとまずここを通過する"""

    # sessionidがなければセットする
    if session.get('sessionid') is None:
        m = hashlib.sha256()
        m.update(os.urandom(64))
        randomStr = m.hexdigest()
        session["sessionid"] = randomStr
    else:
        pass


@app.route("/")
def hello():
    """topページを表示"""

    title = u"ようこそ"
    productDao = ProductDao()
    products = productDao.getAllProduct()
    sample = random.sample(products, 6)
    message = "Webcome to FlowerFlower!"
    return render_template("index.html", title=title, message=message, products=sample)


@app.route("/all", methods=["GET", "POST"])
def all():
    """全商品表示画面を表示"""

    title = u"こんにちは"

    # 全商品情報を取得する
    productDao = ProductDao()
    products = productDao.getAllProduct()

    # index.html をレンダリングする
    return render_template('all_products.html',
                           title=title, products=products)


@app.route("/detail/<int:id>", methods=["GET", "POST"])
def detail(id):
    """商品詳細画面を表示"""
    title = u"商品詳細画面"

    # 指定されたidで商品を検索する
    product = None
    productDao = ProductDao()
    product = productDao.getProductDetail(id)

    return render_template('detail.html', title=title, product=product)


@app.route("/recommend", methods=["GET", "POST"])
def recommend():
    """お勧め画面を表示"""

    title = u"お勧め商品"

    # レコメンドフラグが経っている商品を取得する
    productDao = ProductDao()
    products = productDao.getRecommendProduct()

    return render_template('recommend.html', title=title, products=products)


@app.route("/search/tag/<string:tag>", methods=["GET", "POST"])
def searchTag(tag):
    """タグで検索"""
    title = u"タグ検索:" + tag

    # 指定されたタグ(キーワード)で検索する
    productDao = ProductDao()
    products = productDao.getProductByTag(tag)

    return render_template('all_products.html', title=title, products=products)


@app.route("/cart/add", methods=["POST"])
def cartAdd():
    u"""カートに商品を追加して、カート画面を表示"""

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

    # DBの更新に成功したかどうかのフラグ
    isSuccess = False

    # 指定された商品がカートに既に入っているかどうかのフラグ
    isExist = False

    # 指定された商品が既にカートに入っているかを確認する
    cartDao = CartDao()
    isExist = cartDao.isExistProduct(session.get("sessionid"), productId)

    # 既に商品がカートに入っていた場合は個数を更新する
    if isExist and productId > 0:
        print("update")
        isSuccess = cartDao.updateCart(session.get("sessionid"), productId, count)

    # カートに商品が入っていなかった場合は追加する
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
    
    カートの全ての商品を表示するために
    def cart()にリダイレクト
    """

    return redirect(url_for("cart"))


@app.route("/cart")
def cart():
    u"""カート画面を表示するための情報を取得して遷移"""
    title = u"カート画面"

    # sessionidに紐づくカートの商品を全て取得する
    cartDao = CartDao()
    cartItems = cartDao.getCart(session.get("sessionid"))

    # 合計金額を計算する
    amount = 0
    for cartItem in cartItems:
        amount += cartItem.amount

    return render_template("cart.html", title=title, cartItems=cartItems, amount=amount)


@app.route("/customerInfo")
def orderInput():
    u"""注文情報入力画面を表示"""
    title = u"注文情報入力画面"
    return render_template("inputCustomerInfo.html", title=title)


@app.route("/customerInfoConfirm", methods=["POST"])
def orderConfirm():
    u"""注文情報確認画面を表示"""
    title = u"注文確認画面"

    isAllInput = True

    if validationUtil.isEmpty(request.form["name"]) == False:
        session["name"] = request.form["name"]
    else:
        isAllInput = False
    if validationUtil.isEmpty(request.form["address"]) == False:
        session["address"] = request.form["address"]
    else:
        isAllInput = False
    if validationUtil.isEmpty(request.form["email"]) == False:
        session["email"] = request.form["email"]
    else:
        isAllInput = False
    if validationUtil.isEmpty(request.form["credit"]) == False:
        session["credit"] = request.form["credit"]
    else:
        isAllInput = False


    if isAllInput == False:
        title = u"注文情報入力画面"
        message = "入力ミスがあります"
        return render_template("inputCustomerInfo.html", title=title, message=message)

    return render_template("inputCustomerConfirm.html", title=title)


@app.route("/orderComplete")
def orderComplete():
    u"""注文完了画面を表示"""

    u"""
    以下のテーブルに登録
    customer
    order
    order_detail
    
    上記は仕様変更のため実施しない
    """

    title = u"注文完了"
    return render_template("orderComplete.html", title=title)


@app.route("/addProduct", methods=["GET", "POST"])
def addProduct():
    u"""商品追加ページの処理"""
    title = u"商品追加ページ"

    name = ""
    price = 0
    recommend = 0
    detail = ""
    tag = ""
    fileName = ""
    randomStr = ""
    productDao = ProductDao()

    if request.method == "POST":
        randomStr = Util.getRandomStr()

        if validationUtil.isEmpty(request.form["name"]) == True:
            name = randomStr
        else:
            name = request.form["name"]

        if validationUtil.isEmpty(request.form["price"]) == False:
            price = request.form["price"]

        if validationUtil.isEmpty(request.form["detail"]) == False:
            detail = request.form["detail"]

        if validationUtil.isEmpty(request.form["recommend"]) == False:
            recommend = request.form["recommend"]

        if validationUtil.isEmpty(request.form["tag"]) == False:
            tag = request.form["tag"]

        if validationUtil.isEmpty(request.files["image_file"]) == False:
            print(request.files['image_file'].filename)

            image_file = request.files['image_file']
            # TODO : 画像ファイルであることを確認する(拡張子の確認ではない)
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(image_file.filename)))

            # tmpディレクトリに作った画像ファイルをimagesディレクトリに移動
            # os.renames(app.config['UPLOAD_FOLDER'] + secure_filename(image_file.filename), app.config['UPLOAD_FOLDER'] + "../" + randomStr + ".jpg")
            shutil.move(app.config['UPLOAD_FOLDER'] + secure_filename(image_file.filename),
                        app.config['UPLOAD_FOLDER'] + "../" + randomStr + ".jpg")

        product = Product()
        product.name = name
        product.price = price
        product.detail = detail
        product.tag = tag
        product.image = randomStr + ".jpg"

        # DBに追加
        productDao.addProduct(product, recommend)

    # HTTP GET
    else:
        pass

    """今までに投稿されたタグを取得する"""
    tags = productDao.getTagList()

    # 商品追加画面を表示
    return render_template("addProduct.html", title=title, tags=tags)


@app.route("/download", methods=["POST"])
def download():
    """指定した画像ファイルをZIP形式でダウンロードするURLにリダイレクトする"""
    title = u"ダウンロード"

    _DOWNLOAD_DIRECTORY = "static/download/"

    cartItems = request.form.getlist("cartItem")

    zipFileName = Util.getRandomStr() + ".zip"
    zipFile = zipfile.ZipFile(zipFileName, "w", zipfile.ZIP_STORED)

    for cartItem in cartItems:
        if validationUtil.isEmpty(cartItem) is False:
            zipFile.write(cartItem)

    zipFile.close()

    os.rename(zipFileName, _DOWNLOAD_DIRECTORY + zipFileName)

    return render_template("download.html", title=title, zipfile=_DOWNLOAD_DIRECTORY + zipFileName)


@app.errorhandler(404)
def not_found(error):
    """404ページ"""
    title = u"page not found"
    return render_template("404.html", title=title)
    pass


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")
