import bdb

from . import home
from app import db
from app.home.forms import LoginForm,RegisterForm
from flask import render_template, url_for, redirect, flash, session

from app.models import User,Books

"""注册"""
@home.route("/register/",methods=["POST", "GET"])
def register():
    form = RegisterForm()  #实例化registerForm
    if form.validate_on_submit():  #提交
        data = form.data  #获取数据
        user = User(
            username = data["username"],
            phone = data["phone"],
            password = data["password"]
            #password = generate_password_hash(data["password"]),  # 对密码加密
        )
        db.session.add(user)   #插入数据
        db.session.commit()    #提交
        return redirect(url_for("home.login"))
    return render_template("home/register.html", form=form)


"""登录"""
@home.route("/login/", methods=["GET", "POST"])
def login():
    if "user_id" in session:        # 如果已经登录，则直接跳转到首页
        return redirect(url_for("home.index"))
    form = LoginForm()              # 实例化LoginForm类
    if form.validate_on_submit():   # 如果提交
        data = form.data            # 接收表单数据
        # 判断手机号是否存在
        user = User.query.filter_by(phone=data["phone"]).first()    # 获取用户信息
        if not user:
            flash("该手机号未被注册使用！", "err")           # 输出错误信息
            return render_template("home/login.html", form=form)  # 返回登录页
        # 判断用户名和密码是否匹配
        if not user.check_password(data["password"]):     # 调用check_password()方法，检测用户名密码是否匹配
            flash("密码错误！", "err")           # 输出错误信息
            return render_template("home/login.html", form=form)  # 返回登录页

        session["user_id"] = user.id                # 将user_id写入session, 后面用户判断用户是否登录
        #session["username"] = userphone.username                # 将user_id写入session, 后面用户判断用户是否登录
        session["userphone"] = user.phone  # 将user_id写入session, 后面用户判断用户是否登录
        return redirect(url_for("home.index")) # 登录成功，跳转到首页
        #return render_template("home/login.html", form=form)  # 返回登录页

    return render_template("home/login.html",form=form) # 渲染登录页面模板

"""登出"""
@home.route("/logout/")
def logout():
    """
    退出登录
    """
    # 重定向到home模块下的登录。
    session.pop("user_id", None)
    session.pop("phone", None)
    return redirect(url_for('home.login'))


"""首页"""
@home.route("/")
def index():
    # 获取10个热门商品
    hot_books = Books.query.order_by(Books.sale_count.desc()).limit(10).all()
    return render_template('home/index.html', hot_books=hot_books) #渲染模板

    # 获取2个热门商品
    # hot_goods = Goods.query.order_by(Goods.views_count.desc()).limit(2).all()
    # # 获取12个新品
    # new_goods = Goods.query.filter_by(is_new=1).order_by(
    #                 Goods.addtime.desc()
    #                     ).limit(12).all()
    # # 获取12个打折商品
    # sale_goods = Goods.query.filter_by(is_sale=1).order_by(
    #                 Goods.addtime.desc()
    #                     ).limit(12).all()
    #hot_goods = Goods
    #print(Goods)
    new_goods = []
    # return render_template('home/index.html',new_goods=new_goods,sale_goods=sale_goods,hot_goods=hot_goods) # 渲染模板
