from app import db
from app import admin
from flask import render_template, redirect, url_for, flash, session, request,jsonify
from app.admin.forms import LoginForm
from app.models import Admin


@admin.route("/login/", methods=["GET","POST"])
def login():
    """
    登录功能
    """
    # 判断是否已经登录
    if "admin" in session:
        return redirect(url_for("admin.index"))
    form = LoginForm()   # 实例化登录表单
    if form.validate_on_submit():   # 验证提交表单
        data = form.data    # 接收数据
        admin = Admin.query.filter_by(manager=data["manager"]).first() # 查找Admin表数据
        # 密码错误时，check_password,则此时not check_password(data["pwd"])为真。
        if not admin.check_password(data["password"]):
            flash("密码错误!", "err")   # 闪存错误信息
            return redirect(url_for("admin.login")) # 跳转到后台登录页
        # 如果是正确的，就要定义session的会话进行保存。
        session["admin"] = data["manager"]  # 存入session
        session["admin_id"] = admin.id # 存入session
        return redirect(url_for("admin.index")) # 返回后台主页
    return render_template("admin/login.html",form=form)