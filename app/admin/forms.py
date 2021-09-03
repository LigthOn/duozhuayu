
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, RadioField,DecimalField,SelectField
from wtforms.validators import DataRequired, ValidationError, Length
"""管理员登录"""
class LoginForm(FlaskForm):
    manager = StringField(
        label="管理员名",
        vaildators=[
            DataRequired("管理员名不能为空")
        ],
        description="管理员名",
        render_kw={
            "class":"manager",
            "placeholder":"请输入管理员名!",
        }
    )
    password = PasswordField(
        label="密码",
        validators=[
            DataRequired("密码不能为空")
        ],
        description="密码",
        render_kw={
            "class": "password",
            "placeholder": "请输入密码！",
        }
    )
    submit = SubmitField(
        '登录',
        render_kw={
            "class": "login_ok",
        }
    )

    # 验证账号，命名规则：validate_ + 字段名。如果要验证密码，则可以创建函数validate_pwd
    def validate_manager(self, field):
        account = field.data
        admin = Admin.query.filter_by(manager=account).count()
        if admin == 0:
            raise ValidationError("账号不存在! ")