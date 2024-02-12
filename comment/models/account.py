# 开发时间：2024/2/11  20:48
# The road is nothing，the end is all    --Demon


from sqlalchemy import ForeignKey
from comment.models import db


# 用户账户的模型类
class Account(db.Model):
    __tablename__ = 't_account'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主键
    # 在当前表增加了一个外键，该外键与user表关联（在数据库中，有外键约束的表叫做从表，当前表为从表）
    userId = db.Column(db.BIGINT, ForeignKey('t_user.id'), doc='用户表主键')
    # db.relationship('User'): 这定义了一个与User模型类的关系。这通常用于表示一对一、一对多或多对多的关系。
    # backref: 允许你通过User模型的accountInfo属性访问这个关系。
    # lazy = True: 这是一个加载策略，表示当你访问这个关系时，应该立即加载相关的对象。
    # uselist=False: 表示这个关系应该返回一个单一的对象，而不是一个列表。这通常用于一对一关系。
    user = db.relationship('User', backref=db.backref('accountInfo', lazy=True, uselist=False))
    total = db.Column(db.Float(10, 2), doc='帐户总额', default=0)
    balance = db.Column(db.Float(10, 2), doc='帐户可余额', default=0)
    frozen = db.Column(db.Float(10, 2), doc='账户总计冻结总额', default=0)
    inverstmentW = db.Column(db.Float(10, 2), doc='总计待收本金', default=0)
    interestTotal = db.Column(db.Float(10, 2), doc='总计待收利息', default=0)
    addCapitalTotal = db.Column(db.Float(10, 2), doc='月投总额', default=0)
    recyclingInterest = db.Column(db.Float(10, 2), doc='月取总额', default=0)
    capitalTotal = db.Column(db.Float(10, 2), doc='月乘总额', default=0)
    inverstmentA = db.Column(db.Float(10, 2), doc='已投资总额', default=0)
    interestA = db.Column(db.Float(10, 2), doc='已赚取利息', default=0)
    uApplyExtractMoney = db.Column(db.Float(10, 2), doc='申请提现金额', default=0)
    discount = db.Column(db.Float(8, 2), doc='代金券的总金额', default=0)
