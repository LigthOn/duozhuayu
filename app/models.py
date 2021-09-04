from app import db
from datetime import datetime


"""用户"""
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    username = db.Column(db.String(45))  # 用户名
    phone = db.Column(db.String(11), unique=True)  # 手机号
    password = db.Column(db.String(100))  # 密码
    # consumption = db.Column(db.DECIMAL(10, 2), default=0)  # 消费额
    # addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 注册时间
    # orders = db.relationship('Orders', backref='user')  # 订单外键关系关联

    def __repr__(self):
        return '<User %r>' % self.name

    def check_password(self, password):
        """
        检测密码是否正确
        :param password: 密码
        :return: 返回布尔值
        """
        #from werkzeug.security import check_password_hash
        #return check_password_hash(self.password, password
        return self.password==password


"""管理员"""
class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)
    manager = db.Column(db.String(45), unique=True)
    password = db.Column(db.String(100))

    def __repr__(self):
        return "<Admin %r>" % self.manager

    def check_password(self, password):
        """
        检测密码是否正确
        :param password: 密码
        :return: 返回布尔值
        """
        return self.password==password


# 书籍
class Books(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    ibsn = db.column(db.String(45))   # IBSN
    name = db.Column(db.String(255))  # 名称
    original_price = db.Column(db.DECIMAL(10,2))  # 原价
    current_price  = db.Column(db.DECIMAL(10,2))  # 现价
    sale_count = db.Column(db.Integer) # 售出的数量
    # picture = db.Column(db.String(255))  # 图片
    # introduction = db.Column(db.Text)  # 商品简介
    # views_count = db.Column(db.Integer,default=0) # 浏览次数
    # is_sale  = db.Column(db.Boolean(), default=0) # 是否特价
    # is_new = db.Column(db.Boolean(), default=0) # 是否新品
    #print(id)
    #print(name)
    # 设置外键
    #supercat_id = db.Column(db.Integer, db.ForeignKey('supercat.id'))  # 所属大分类
    #subcat_id = db.Column(db.Integer, db.ForeignKey('subcat.id'))  # 所属小分类
    #addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    #cart = db.relationship("Cart", backref='goods')  # 订单外键关系关联
    #orders_detail = db.relationship("OrdersDetail", backref='goods')  # 订单外键关系关联

    def __repr__(self):
        return "<Goods %r>" % self.name