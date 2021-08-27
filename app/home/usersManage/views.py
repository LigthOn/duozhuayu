from app.home import usersManage
from app.home.usersManage.forms import LoginForm
from flask import render_template, url_for, redirect, flash, session

from app.models import User

"""登录"""
@usersManage.route("/login/", methods=["GET", "POST"])
def login():
    if "user_id" in session:        # 如果已经登录，则直接跳转到首页
        return redirect(url_for("home.index"))
    form = LoginForm()              # 实例化LoginForm类
    if form.validate_on_submit():   # 如果提交
        data = form.data            # 接收表单数据
        # 判断手机号是否存在
        userphone = User.query.filter_by(phont=data["phone"]).first()    # 获取用户信息
        if not userphone:
            flash("该手机号未被注册使用！", "err")           # 输出错误信息
            return render_template("home/login.html", form=form)  # 返回登录页
        # 判断用户名和密码是否匹配
        if not userphone.check_password(data["password"]):     # 调用check_password()方法，检测用户名密码是否匹配
            flash("密码错误！", "err")           # 输出错误信息
            return render_template("home/login.html", form=form)  # 返回登录页

        session["user_id"] = userphone.id                # 将user_id写入session, 后面用户判断用户是否登录
        session["username"] = userphone.username                # 将user_id写入session, 后面用户判断用户是否登录
        return redirect(url_for("home.index")) # 登录成功，跳转到首页

    return render_template("home/login.html",form=form) # 渲染登录页面模板