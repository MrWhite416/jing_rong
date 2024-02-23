# 开发时间：2024/2/22  19:42
# The road is nothing，the end is all    --Demon

from sqlalchemy import ForeignKey
from comment.models import db



# 银行卡信息的模型类
class BankCard(db.Model):
    __tablename__ = 't_bankcard'
    bankInfoId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bankCardNum = db.Column(db.String(64), comment='银行卡号')
    openingBank = db.Column(db.String(64), comment='开户银行')
    cityId = db.Column(db.Integer, comment='城市id')
    userId = db.Column(db.BIGINT, ForeignKey('t_user.id'), comment='用户表主键')
    user = db.relationship('User', backref=db.backref('bankCards', lazy=True))
    bankId = db.Column(db.Integer, comment='银行编号')
    bankBranch = db.Column(db.String(64), comment='银行支行')
    reservePhone = db.Column(db.String(64), comment='绑定手机号码')