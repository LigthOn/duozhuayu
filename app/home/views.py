import bdb

from . import home
from app import db
from app.home.forms import LoginForm,RegisterForm,AddressForm
from flask import render_template, url_for, redirect, flash, session, request
from functools import wraps

from app.models import User,Books, Cart, Orders,OrdersDetail

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


def user_login(f):
    """
    登录装饰器
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("home.login"))
        return f(*args, **kwargs)

    return decorated_function

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
    return redirect(url_for('home.index'))


"""首页"""
@home.route("/")
def index():
    # 获取10个热门商品
    hot_books = Books.query.order_by(Books.sale_count.desc()).limit(4).all()
    #print(hot_books[0].name)
    # print("hello")
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


"""搜索框"""
@home.route("/search")
def search():
    page = request.args.get('page', 1, type=int) # 获取page参数值
    keywords = request.args.get('keywords','',type=str)

    if keywords :
        # 使用like实现模糊查询
        page_data = Books.query.filter(Books.name.like("%"+keywords+"%")).order_by(
            Books.addtime.desc()
        ).paginate(page=page, per_page=12)
    else :
        page_data = Books.query.order_by(
            Books.addtime.desc()
        ).paginate(page=page, per_page=12)
    hot_goods = Books.query.order_by(Books.views_count.desc()).limit(7).all()
    return render_template("home/goods_search.html", page_data=page_data,keywords=keywords,hot_goods=hot_goods)


"""书籍详情页"""
@home.route("/books_detail/<int:id>/")
def books_detail(id=None):  # id 为商品ID
    """
    详情页
    """
    user_id = session.get('user_id', 0)  # 获取用户ID,判断用户是否登录
    book= Books.query.get_or_404(id) # 根据景区ID获取景区数据，如果不存在返回404
    # 浏览量加1
    book.views_count += 1
    db.session.add(book) # 添加数据
    db.session.commit()   # 提交数据
    return render_template('home/books_detail.html',book=book,user_id=user_id)   # 渲染模板


@home.route("/cart_add/")
@user_login
def cart_add():
    """
    添加购物车
    """
    book_id = request.args.get('book_id'),
    quantity = request.args.get('quantity'),
    user_id = session.get('user_id', 0)  # 获取用户ID,判断用户是否登录
    print(user_id)
    # cart = Cart.query.filter_by(user_id=user_id).update({'user_id': 0})
    # cart = Cart.query.filter_by(book_id=book_id).first()
    cart = Cart.query.filter_by(user_id=user_id, book_id=book_id).first()
    if cart:
        curr_quantity = cart.quantity
        total = curr_quantity+int(quantity[0])
        cart.quantity = total
    else:
        cart = Cart(
            book_id = request.args.get('book_id'),
            quantity = request.args.get('quantity'),
            user_id=user_id  # 获取用户ID,判断用户是否登录
        )
        print(user_id)
        db.session.add(cart) # 添加数据
        db.session.commit()  # 提交数据
    db.session.commit()   # 提交数据
    return redirect(url_for('home.shopping_cart'))

@home.route("/shopping_cart/")
@user_login
def shopping_cart():
    user_id = session.get('user_id',0)
    cart = Cart.query.filter_by(user_id = int(user_id)).all()
    if cart:
        return render_template('home/cart.html',cart=cart, user_id=user_id)
    else:
        return render_template('home/cart.html')


@home.route("/cart_update/")
@user_login
def cart_update():
    """
    添加购物车
    """
    book_id = request.args.get('book_id'),
    quantity = request.args.get('quantity'),
    print(quantity)
    user_id = session.get('user_id', 0)  # 获取用户ID,判断用户是否登录

    # cart = Cart.query.filter_by(user_id=user_id).update({'user_id': 0})
    cart = Cart.query.filter_by(book_id=book_id).first()

    cart.quantity = quantity

    db.session.commit()  # 提交数据
    return redirect(url_for('home.shopping_cart'))



"""登录"""
@home.route("/order_add/", methods=["GET", "POST"])
@user_login
def order_add():
    user_id = session.get('user_id', 0)
    form = AddressForm()
    if form.validate_on_submit():   # 如果提交
        data = form.data            # 接收表单数据

        orders = Orders(
            user_id=user_id,
            receive_name=data["receivename"],
            receive_phone=data["phone"],
            receive_address=data["receiveaddress"]
        )
        db.session.add(orders)
        db.session.commit()

        #添加订单详情
        cart = Cart.query.filter_by(user_id=user_id).all()
        object = []
        for item in cart:
            object.append(
                OrdersDetail(
                    order_id=orders.id,
                    book_id=item.book_id,
                    quantity=item.quantity, )
            )
        db.session.add_all(object)
        # 更改购物车状态
        Cart.query.filter_by(user_id=user_id).update({'user_id': 0})
        db.session.commit()
        # return redirect(url_for('home.index'))
        return redirect(url_for('home.order_list'))
    return render_template("home/addaddress.html", form=form)


@home.route("/order_list/",methods=['GET','POST'])
@user_login
def order_list():
    """"
    我的订单
    """
    user_id = session.get('user_id',0)
    orders = Orders.query.filter_by(user_id=user_id).all()
    return render_template('home/order_list.html',orders=orders)

@home.route("/order_detail_list/",methods=['GET','POST'])
@user_login
def order_detail_list():
    """"
    我的订单
    """
    user_id = session.get('user_id',0)
    order_id = request.args.get('orderid')
    # orders = OrdersDetail.query.join(Orders).filter(Orders.user_id==user_id).all()
    orders = OrdersDetail.query.filter_by(order_id=order_id).all();
    return render_template('home/order_detail_list.html',orders=orders)


@home.route("/order_delete/", methods=["GET", "POST"])
@user_login
def order_delete():
    order_id = request.args.get('orderid')
    OrdersDetail.query.filter_by(order_id=order_id).delete()
    db.session.commit()
    Orders.query.filter_by(id=order_id).delete()
    db.session.commit()
    return redirect(url_for('home.order_list'))

@home.route("/book_delete/", methods=["GET", "POST"])
@user_login
def book_delete():
    book_id = request.args.get('bookid')
    Cart.query.filter_by(book_id=book_id).delete()
    db.session.commit()
    return redirect(url_for('home.shopping_cart'))