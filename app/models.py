from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    username = db.Column(db.String(100)) # 用户名
    password = db.Column(db.String(100))  # 密码
    email = db.Column(db.String(100), unique=True)  # 邮箱
    phone = db.Column(db.String(11), unique=True)  # 手机号
    consumption = db.Column(db.DECIMAL(10, 2), default=0)  # 消费额
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 注册时间
    orders = db.relationship('Orders', backref='user')  # 订单外键关系关联

    def __repr__(self):
        return '<User %r>' % self.name

    def check_password(self, password):
        """
        检测密码是否正确
        :param password: 密码
        :return: 返回布尔值
        """
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password, password)